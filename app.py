from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Booking, ClassModel, Member, Payment, Trainer, db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'

db.init_app(app)


def parse_date(value, field_name):
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except (ValueError, TypeError):
        raise ValueError(f'Invalid {field_name}. Use YYYY-MM-DD.')


def parse_time(value, field_name):
    try:
        return datetime.strptime(value, '%H:%M').time()
    except (ValueError, TypeError):
        raise ValueError(f'Invalid {field_name}. Use HH:MM.')


def parse_decimal(value, field_name):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError):
        raise ValueError(f'Invalid {field_name}. Enter a valid number.')
    return result


def not_blank(value, field_name):
    if value is None or not str(value).strip():
        raise ValueError(f'{field_name} is required.')
    return str(value).strip()


@app.before_request
def create_tables_once():
    db.create_all()


@app.route('/')
def index():
    total_members = db.session.query(func.count(Member.member_id)).scalar() or 0
    total_trainers = db.session.query(func.count(Trainer.trainer_id)).scalar() or 0
    total_classes = db.session.query(func.count(ClassModel.class_id)).scalar() or 0
    total_bookings = db.session.query(func.count(Booking.booking_id)).scalar() or 0
    total_revenue = db.session.query(func.coalesce(func.sum(Payment.amount - Payment.discount), 0)).scalar() or 0
    avg_payment = db.session.query(func.coalesce(func.avg(Payment.amount - Payment.discount), 0)).scalar() or 0

    class_counts = (
        db.session.query(
            ClassModel.class_id,
            ClassModel.class_name,
            ClassModel.class_date,
            ClassModel.capacity,
            func.count(Booking.booking_id).label('booking_count'),
        )
        .outerjoin(Booking, Booking.class_id == ClassModel.class_id)
        .group_by(ClassModel.class_id)
        .order_by(ClassModel.class_date.asc(), ClassModel.start_time.asc())
        .all()
    )

    recent_payments = Payment.query.order_by(Payment.payment_date.desc(), Payment.payment_id.desc()).limit(5).all()

    return render_template(
        'index.html',
        total_members=total_members,
        total_trainers=total_trainers,
        total_classes=total_classes,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        avg_payment=avg_payment,
        class_counts=class_counts,
        recent_payments=recent_payments,
    )


@app.route('/members')
def members():
    all_members = Member.query.order_by(Member.last_name.asc(), Member.first_name.asc()).all()
    return render_template('members.html', members=all_members)


@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        try:
            member = Member(
                first_name=not_blank(request.form.get('first_name'), 'First name'),
                last_name=not_blank(request.form.get('last_name'), 'Last name'),
                email=not_blank(request.form.get('email'), 'Email'),
                phone=request.form.get('phone', '').strip(),
                join_date=parse_date(request.form.get('join_date'), 'join date'),
                membership_type=not_blank(request.form.get('membership_type'), 'Membership type'),
                status=not_blank(request.form.get('status'), 'Status'),
                record_source=not_blank(request.form.get('record_source'), 'Record source'),
            )
            db.session.add(member)
            db.session.commit()
            flash('Member added successfully.', 'success')
            return redirect(url_for('members'))
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            flash('Could not add member: ' + str(e), 'danger')
    return render_template('member_form.html', member=None, today=date.today().isoformat())


@app.route('/members/edit/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    member = Member.query.get_or_404(member_id)
    if request.method == 'POST':
        try:
            member.first_name = not_blank(request.form.get('first_name'), 'First name')
            member.last_name = not_blank(request.form.get('last_name'), 'Last name')
            member.email = not_blank(request.form.get('email'), 'Email')
            member.phone = request.form.get('phone', '').strip()
            member.join_date = parse_date(request.form.get('join_date'), 'join date')
            member.membership_type = not_blank(request.form.get('membership_type'), 'Membership type')
            member.status = not_blank(request.form.get('status'), 'Status')
            member.record_source = not_blank(request.form.get('record_source'), 'Record source')
            db.session.commit()
            flash('Member updated successfully.', 'success')
            return redirect(url_for('members'))
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            flash('Could not update member: ' + str(e), 'danger')
    return render_template('member_form.html', member=member, today=date.today().isoformat())


@app.route('/members/delete/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    member = Member.query.get_or_404(member_id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Member deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete member: ' + str(e), 'danger')
    return redirect(url_for('members'))


@app.route('/trainers')
def trainers():
    all_trainers = Trainer.query.order_by(Trainer.last_name.asc(), Trainer.first_name.asc()).all()
    return render_template('trainers.html', trainers=all_trainers)


@app.route('/trainers/add', methods=['GET', 'POST'])
def add_trainer():
    if request.method == 'POST':
        try:
            hourly_rate = parse_decimal(request.form.get('hourly_rate'), 'hourly rate')
            if hourly_rate < 0:
                raise ValueError('Hourly rate cannot be negative.')
            trainer = Trainer(
                first_name=not_blank(request.form.get('first_name'), 'First name'),
                last_name=not_blank(request.form.get('last_name'), 'Last name'),
                specialty=not_blank(request.form.get('specialty'), 'Specialty'),
                hire_date=parse_date(request.form.get('hire_date'), 'hire date'),
                certification_level=not_blank(request.form.get('certification_level'), 'Certification level'),
                hourly_rate=hourly_rate,
                record_source=not_blank(request.form.get('record_source'), 'Record source'),
            )
            db.session.add(trainer)
            db.session.commit()
            flash('Trainer added successfully.', 'success')
            return redirect(url_for('trainers'))
        except ValueError as e:
            db.session.rollback()
            flash('Could not add trainer: ' + str(e), 'danger')
    return render_template('trainer_form.html', trainer=None, today=date.today().isoformat())


@app.route('/trainers/edit/<int:trainer_id>', methods=['GET', 'POST'])
def edit_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    if request.method == 'POST':
        try:
            hourly_rate = parse_decimal(request.form.get('hourly_rate'), 'hourly rate')
            if hourly_rate < 0:
                raise ValueError('Hourly rate cannot be negative.')
            trainer.first_name = not_blank(request.form.get('first_name'), 'First name')
            trainer.last_name = not_blank(request.form.get('last_name'), 'Last name')
            trainer.specialty = not_blank(request.form.get('specialty'), 'Specialty')
            trainer.hire_date = parse_date(request.form.get('hire_date'), 'hire date')
            trainer.certification_level = not_blank(request.form.get('certification_level'), 'Certification level')
            trainer.hourly_rate = hourly_rate
            trainer.record_source = not_blank(request.form.get('record_source'), 'Record source')
            db.session.commit()
            flash('Trainer updated successfully.', 'success')
            return redirect(url_for('trainers'))
        except ValueError as e:
            db.session.rollback()
            flash('Could not update trainer: ' + str(e), 'danger')
    return render_template('trainer_form.html', trainer=trainer, today=date.today().isoformat())


@app.route('/trainers/delete/<int:trainer_id>', methods=['POST'])
def delete_trainer(trainer_id):
    trainer = Trainer.query.get_or_404(trainer_id)
    try:
        db.session.delete(trainer)
        db.session.commit()
        flash('Trainer deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete trainer. Delete that trainer\'s classes first. Details: ' + str(e), 'danger')
    return redirect(url_for('trainers'))


@app.route('/classes')
def classes():
    all_classes = ClassModel.query.order_by(ClassModel.class_date.asc(), ClassModel.start_time.asc()).all()
    return render_template('classes.html', classes=all_classes)


@app.route('/classes/add', methods=['GET', 'POST'])
def add_class():
    trainers = Trainer.query.order_by(Trainer.last_name.asc()).all()
    if request.method == 'POST':
        try:
            capacity = int(request.form.get('capacity', 0))
            if capacity < 0:
                raise ValueError('Capacity cannot be negative.')
            gym_class = ClassModel(
                trainer_id=int(request.form.get('trainer_id')),
                class_name=not_blank(request.form.get('class_name'), 'Class name'),
                class_level=not_blank(request.form.get('class_level'), 'Class level'),
                room_name=not_blank(request.form.get('room_name'), 'Room name'),
                class_date=parse_date(request.form.get('class_date'), 'class date'),
                start_time=parse_time(request.form.get('start_time'), 'start time'),
                capacity=capacity,
                record_source=not_blank(request.form.get('record_source'), 'Record source'),
            )
            db.session.add(gym_class)
            db.session.commit()
            flash('Class added successfully.', 'success')
            return redirect(url_for('classes'))
        except (ValueError, TypeError) as e:
            db.session.rollback()
            flash('Could not add class: ' + str(e), 'danger')
    return render_template('class_form.html', gym_class=None, trainers=trainers, today=date.today().isoformat())


@app.route('/classes/edit/<int:class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    gym_class = ClassModel.query.get_or_404(class_id)
    trainers = Trainer.query.order_by(Trainer.last_name.asc()).all()
    if request.method == 'POST':
        try:
            capacity = int(request.form.get('capacity', 0))
            if capacity < 0:
                raise ValueError('Capacity cannot be negative.')
            current_bookings = Booking.query.filter_by(class_id=class_id).count()
            if capacity < current_bookings:
                raise ValueError('Capacity cannot be lower than the number of existing bookings.')
            gym_class.trainer_id = int(request.form.get('trainer_id'))
            gym_class.class_name = not_blank(request.form.get('class_name'), 'Class name')
            gym_class.class_level = not_blank(request.form.get('class_level'), 'Class level')
            gym_class.room_name = not_blank(request.form.get('room_name'), 'Room name')
            gym_class.class_date = parse_date(request.form.get('class_date'), 'class date')
            gym_class.start_time = parse_time(request.form.get('start_time'), 'start time')
            gym_class.capacity = capacity
            gym_class.record_source = not_blank(request.form.get('record_source'), 'Record source')
            db.session.commit()
            flash('Class updated successfully.', 'success')
            return redirect(url_for('classes'))
        except (ValueError, TypeError) as e:
            db.session.rollback()
            flash('Could not update class: ' + str(e), 'danger')
    return render_template('class_form.html', gym_class=gym_class, trainers=trainers, today=date.today().isoformat())


@app.route('/classes/delete/<int:class_id>', methods=['POST'])
def delete_class(class_id):
    gym_class = ClassModel.query.get_or_404(class_id)
    try:
        db.session.delete(gym_class)
        db.session.commit()
        flash('Class deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete class: ' + str(e), 'danger')
    return redirect(url_for('classes'))


@app.route('/bookings')
def bookings():
    all_bookings = Booking.query.order_by(Booking.booking_date.desc(), Booking.booking_id.desc()).all()
    return render_template('bookings.html', bookings=all_bookings)


@app.route('/bookings/add', methods=['GET', 'POST'])
def add_booking():
    members = Member.query.order_by(Member.last_name.asc(), Member.first_name.asc()).all()
    classes = ClassModel.query.order_by(ClassModel.class_date.asc(), ClassModel.start_time.asc()).all()
    if request.method == 'POST':
        try:
            member_id = int(request.form.get('member_id'))
            class_id = int(request.form.get('class_id'))
            attendance_status = not_blank(request.form.get('attendance_status'), 'Attendance status')
            record_source = not_blank(request.form.get('record_source'), 'Record source')
            booking_date = parse_date(request.form.get('booking_date'), 'booking date')
            notes = request.form.get('notes', '').strip()

            member = Member.query.get(member_id)
            gym_class = ClassModel.query.get(class_id)
            if not member or not gym_class:
                raise ValueError('Selected member or class does not exist.')

            existing_booking = Booking.query.filter_by(member_id=member_id, class_id=class_id).first()
            if existing_booking:
                raise ValueError('This member is already booked in that class.')

            current_bookings = Booking.query.filter_by(class_id=class_id).count()
            if current_bookings >= gym_class.capacity:
                raise ValueError('This class is already full.')

            booking = Booking(
                member_id=member_id,
                class_id=class_id,
                booking_date=booking_date,
                attendance_status=attendance_status,
                notes=notes,
                record_source=record_source,
            )
            db.session.add(booking)
            db.session.commit()
            flash('Booking created successfully.', 'success')
            return redirect(url_for('bookings'))
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            flash('Could not create booking: ' + str(e), 'danger')
    return render_template('booking_form.html', booking=None, members=members, classes=classes, today=date.today().isoformat())


@app.route('/bookings/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    try:
        db.session.delete(booking)
        db.session.commit()
        flash('Booking deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete booking: ' + str(e), 'danger')
    return redirect(url_for('bookings'))


@app.route('/payments')
def payments():
    all_payments = Payment.query.order_by(Payment.payment_date.desc(), Payment.payment_id.desc()).all()
    return render_template('payments.html', payments=all_payments)


@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    members = Member.query.order_by(Member.last_name.asc(), Member.first_name.asc()).all()
    if request.method == 'POST':
        try:
            amount = parse_decimal(request.form.get('amount'), 'amount')
            discount = parse_decimal(request.form.get('discount'), 'discount')
            if amount < 0:
                raise ValueError('Amount cannot be negative.')
            if discount < 0:
                raise ValueError('Discount cannot be negative.')
            if discount > amount:
                raise ValueError('Discount cannot be greater than amount.')
            payment = Payment(
                member_id=int(request.form.get('member_id')),
                payment_date=parse_date(request.form.get('payment_date'), 'payment date'),
                amount=amount,
                discount=discount,
                payment_method=not_blank(request.form.get('payment_method'), 'Payment method'),
                payment_status=not_blank(request.form.get('payment_status'), 'Payment status'),
                record_source=not_blank(request.form.get('record_source'), 'Record source'),
            )
            db.session.add(payment)
            db.session.commit()
            flash('Payment added successfully.', 'success')
            return redirect(url_for('payments'))
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            flash('Could not add payment: ' + str(e), 'danger')
    return render_template('payment_form.html', payment=None, members=members, today=date.today().isoformat())


@app.route('/payments/edit/<int:payment_id>', methods=['GET', 'POST'])
def edit_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    members = Member.query.order_by(Member.last_name.asc(), Member.first_name.asc()).all()
    if request.method == 'POST':
        try:
            amount = parse_decimal(request.form.get('amount'), 'amount')
            discount = parse_decimal(request.form.get('discount'), 'discount')
            if amount < 0:
                raise ValueError('Amount cannot be negative.')
            if discount < 0:
                raise ValueError('Discount cannot be negative.')
            if discount > amount:
                raise ValueError('Discount cannot be greater than amount.')
            payment.member_id = int(request.form.get('member_id'))
            payment.payment_date = parse_date(request.form.get('payment_date'), 'payment date')
            payment.amount = amount
            payment.discount = discount
            payment.payment_method = not_blank(request.form.get('payment_method'), 'Payment method')
            payment.payment_status = not_blank(request.form.get('payment_status'), 'Payment status')
            payment.record_source = not_blank(request.form.get('record_source'), 'Record source')
            db.session.commit()
            flash('Payment updated successfully.', 'success')
            return redirect(url_for('payments'))
        except (ValueError, IntegrityError) as e:
            db.session.rollback()
            flash('Could not update payment: ' + str(e), 'danger')
    return render_template('payment_form.html', payment=payment, members=members, today=date.today().isoformat())


@app.route('/payments/delete/<int:payment_id>', methods=['POST'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    try:
        db.session.delete(payment)
        db.session.commit()
        flash('Payment deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Could not delete payment: ' + str(e), 'danger')
    return redirect(url_for('payments'))


@app.route('/members/<int:member_id>')
def member_detail(member_id):
    member = Member.query.get_or_404(member_id)
    return render_template('member_detail.html', member=member)


@app.route('/classes/<int:class_id>')
def class_detail(class_id):
    gym_class = ClassModel.query.get_or_404(class_id)
    booking_count = Booking.query.filter_by(class_id=class_id).count()
    return render_template('class_detail.html', gym_class=gym_class, booking_count=booking_count)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
