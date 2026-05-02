# 3rd Normal Form Report

## Project 2 Reference
This Project 3 application directly continues Project 2. The original Project 2 database design used the following entities:
- members
- payments
- bookings
- classes
- trainers

## Original Functional Dependencies
Below are the key functional dependencies used in the design.

### Members
- `member_id -> first_name, last_name, email, phone, join_date, membership_type, status, record_source, created_at`

### Payments
- `payment_id -> member_id, payment_date, amount, discount, payment_method, payment_status, record_source, created_at`

### Trainers
- `trainer_id -> first_name, last_name, specialty, hire_date, certification_level, hourly_rate, record_source, created_at`

### Classes
- `class_id -> trainer_id, class_name, class_level, room_name, class_date, start_time, capacity, record_source, created_at`

### Bookings
- `booking_id -> member_id, class_id, booking_date, attendance_status, notes, record_source, created_at`

## Anomaly Identification
A single large unnormalized table for the entire gym system would create several problems.

### Update Anomaly
If trainer information appeared in multiple class rows, updating a trainer's specialty or hourly rate would require changes in many places.

### Insertion Anomaly
If payment and booking information were stored in the same table as member and class details, it would be difficult to add a new trainer or class before any bookings existed.

### Deletion Anomaly
If the last booking for a class were deleted from a large combined table, important class or trainer information could also be lost.

## Decomposition Steps
To remove redundancy and preserve data integrity, the design was decomposed into smaller relations.

### Step 1: Separate Member Data
All member-specific attributes were placed into the `members` table.

### Step 2: Separate Trainer Data
All trainer-specific attributes were placed into the `trainers` table.

### Step 3: Separate Class Data
Class-specific attributes were placed into the `classes` table, with `trainer_id` used as a foreign key.

### Step 4: Separate Payment Data
Payment records were placed into the `payments` table, with `member_id` used as a foreign key.

### Step 5: Use a Booking Table for the Relationship
The `bookings` table was used to connect members and classes. This resolves the many-bookings structure cleanly while allowing attendance and notes to be stored with the booking itself.

## Why the Final Schema Is in 3NF
The final schema satisfies 3NF because:
- each table has a primary key
- every non-key attribute depends on the whole key
- there are no repeating groups
- there are no transitive dependencies between non-key attributes inside the same table
- relationship data is separated using foreign keys

## Final Relational Schema
### members
`members(member_id, first_name, last_name, email, phone, join_date, membership_type, status, record_source, created_at)`

### trainers
`trainers(trainer_id, first_name, last_name, specialty, hire_date, certification_level, hourly_rate, record_source, created_at)`

### classes
`classes(class_id, trainer_id, class_name, class_level, room_name, class_date, start_time, capacity, record_source, created_at)`

### bookings
`bookings(booking_id, member_id, class_id, booking_date, attendance_status, notes, record_source, created_at)`

### payments
`payments(payment_id, member_id, payment_date, amount, discount, payment_method, payment_status, record_source, created_at)`

## Final Notes
This final schema is the schema used by  Python in Project 3. It is a direct continuation of the Project 2 ERD and preserves the original gym management subject while improving implementation readiness and integrity.
