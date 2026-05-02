INSERT INTO members (first_name, last_name, email, phone, join_date, membership_type, status, record_source)
VALUES
('Ava', 'Johnson', 'ava.johnson@example.com', '316-555-1001', '2026-01-10', 'Premium', 'Active', 'Seed Data'),
('Liam', 'Martinez', 'liam.martinez@example.com', '316-555-1002', '2026-02-01', 'Basic', 'Active', 'Seed Data'),
('Sophia', 'Brown', 'sophia.brown@example.com', '316-555-1003', '2026-02-14', 'Student', 'Active', 'Seed Data');

INSERT INTO trainers (first_name, last_name, specialty, hire_date, certification_level, hourly_rate, record_source)
VALUES
('Noah', 'Clark', 'Strength Training', '2025-08-15', 'Level 2', 35.00, 'Seed Data'),
('Emma', 'Davis', 'Yoga', '2025-06-20', 'Level 3', 40.00, 'Seed Data');

INSERT INTO classes (trainer_id, class_name, class_level, room_name, class_date, start_time, capacity, record_source)
VALUES
(1, 'Morning Strength', 'Intermediate', 'Studio A', '2026-05-02', '08:00', 12, 'Seed Data'),
(2, 'Evening Yoga', 'Beginner', 'Studio B', '2026-05-02', '18:00', 15, 'Seed Data');

INSERT INTO bookings (member_id, class_id, booking_date, attendance_status, notes, record_source)
VALUES
(1, 1, '2026-05-01', 'Booked', 'First visit', 'Seed Data'),
(2, 2, '2026-05-01', 'Booked', 'Needs yoga mat', 'Seed Data');

INSERT INTO payments (member_id, payment_date, amount, discount, payment_method, payment_status, record_source)
VALUES
(1, '2026-05-01', 75.00, 5.00, 'Card', 'Completed', 'Seed Data'),
(2, '2026-05-01', 50.00, 0.00, 'Cash', 'Completed', 'Seed Data');
