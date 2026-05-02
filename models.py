from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, func


db = SQLAlchemy()


class Member(db.Model):
    __tablename__ = 'members'

    member_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone = db.Column(db.String(30))
    join_date = db.Column(db.Date, nullable=False)
    membership_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Active')
    record_source = db.Column(db.String(50), nullable=False, default='Web App')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    payments = db.relationship('Payment', back_populates='member', cascade='all, delete-orphan')
    bookings = db.relationship('Booking', back_populates='member', cascade='all, delete-orphan')


class Trainer(db.Model):
    __tablename__ = 'trainers'

    trainer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    certification_level = db.Column(db.String(100), nullable=False)
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    record_source = db.Column(db.String(50), nullable=False, default='Web App')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('hourly_rate >= 0', name='ck_trainers_hourly_rate_nonnegative'),
    )

    classes = db.relationship('ClassModel', back_populates='trainer', cascade='all, delete-orphan')


class ClassModel(db.Model):
    __tablename__ = 'classes'

    class_id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.trainer_id', ondelete='RESTRICT'), nullable=False)
    class_name = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(50), nullable=False)
    room_name = db.Column(db.String(100), nullable=False)
    class_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    record_source = db.Column(db.String(50), nullable=False, default='Web App')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('capacity >= 0', name='ck_classes_capacity_nonnegative'),
    )

    trainer = db.relationship('Trainer', back_populates='classes')
    bookings = db.relationship('Booking', back_populates='gym_class', cascade='all, delete-orphan')


class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id', ondelete='CASCADE'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    attendance_status = db.Column(db.String(50), nullable=False, default='Booked')
    notes = db.Column(db.String(255))
    record_source = db.Column(db.String(50), nullable=False, default='Web App')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        UniqueConstraint('member_id', 'class_id', name='uq_member_class_booking'),
    )

    member = db.relationship('Member', back_populates='bookings')
    gym_class = db.relationship('ClassModel', back_populates='bookings')


class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('members.member_id', ondelete='CASCADE'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), nullable=False, default='Completed')
    record_source = db.Column(db.String(50), nullable=False, default='Web App')
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('amount >= 0', name='ck_payments_amount_nonnegative'),
        CheckConstraint('discount >= 0', name='ck_payments_discount_nonnegative'),
    )

    member = db.relationship('Member', back_populates='payments')
