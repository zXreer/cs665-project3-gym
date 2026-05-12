INSERT INTO members (first_name, last_name, email, phone, join_date, membership_type, status, record_source)
VALUES
('Zareer', 'Khan', 'zareer.khan@email.com', '316-420-6700', '2026-01-01', 'Gold', 'Active', 'Seed Data'),
('Maya', 'Nawar', 'maya.nawar@email.com', '316-440-7700', '2026-03-01', 'Silver', 'Active', 'Seed Data'),
('Leo', 'Carter', 'leo.carter@email.com', '316-410-8700', '2026-01-24', 'Premium', 'Active', 'Seed Data');

INSERT INTO trainers (first_name, last_name, specialty, hire_date, certification_level, hourly_rate, record_source)
VALUES
('Jack', 'Tomlinson', 'Strength', '2024-06-07', 'Senior', 45.00, 'Seed Data'),
('Chris', 'Bumstead', 'Strength', '2022-09-10', 'Master', 60.00, 'Seed Data');

INSERT INTO classes (trainer_id, class_name, class_level, room_name, class_date, start_time, capacity, record_source)
VALUES
(1, 'Strength Basics', 'Beginenr', 'Weight Room', '2026-03-15', '10:00', 20, 'Seed Data'),
(2, 'Bodybuilding Advanced', 'Advanced', 'Weight Room', '2026-03-16', '17:00', 10, 'Seed Data');

INSERT INTO bookings (member_id, class_id, booking_date, attendance_status, notes, record_source)
VALUES
(1, 1, '2026-03-10', 'Attended', 'Arrived on time', 'Seed Data'),
(2, 2, '2026-03-11', 'Attended', 'First visit', 'Seed Data');

INSERT INTO payments (member_id, payment_date, amount, discount, payment_method, payment_status, record_source)
VALUES
(1, '2026-03-01', 80.00, 5.00, 'Card', 'Paid', 'Seed Data'),
(2, '2026-03-02', 60.00, 0.00, 'Cash', 'Paid', 'Seed Data');
