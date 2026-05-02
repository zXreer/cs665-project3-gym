# Gym Membership Management System

This project is a continuation of **Project 2**. In Project 2, I designed the database for a gym membership management scenario using the tables **members, payments, bookings, classes, and trainers**. In Project 3, I implemented the database as a full-stack Python web application.

## Project Description
This application helps gym staff manage:
- members
- trainers
- classes
- bookings
- payments
- dashboard summaries

The project uses a normalized relational database and provides a clean web interface for managing related records.

## Technology Stack
- Python 3
- Flask
- SQLite
- SQLAlchemy
- HTML5
- CSS3
- Bootstrap 5
- Jinja2
- Git

## Features
- CRUD for members, trainers, classes, and payments
- Booking management between members and classes
- Relationship views for members and classes
- Transaction/business logic that prevents overbooking
- Server-side validation for bad data
- Dashboard with COUNT, SUM, and AVG summary queries

## Softwares that has been used
- **VS Code** for editing the project
- **Python 3** to run the app
- **Terminal** to run commands
- **Git** for commit history
- **GitHub** to upload the repository
- **Chrome or Safari** to view the app
- **DB Browser for SQLite** to inspect the database visually

## Installation Instructions
1. Open the folder in VS Code.
2. Open a terminal in the project folder.
3. Create a virtual environment.
4. Activate it:

'python3 
5. Install dependencies:

   'pip install -r requirements.txt'

6. Run the application:

   'python3 app.py'

7. Open your browser at:
   
   'http://127.0.0.1:5000/'

## Database Setup
This application uses SQLite and creates the database automatically the first time it runs.

If you want to review the final schema separately, use:
- `schema.sql`

If you want sample data ideas, use:
- `seed.sql`

## Main Pages
- `/` dashboard
- `/members`
- `/trainers`
- `/classes`
- `/bookings`
- `/payments`

## Usage Notes
- Add trainers before creating classes.
- Add members and classes before creating bookings.
- A member cannot be booked into the same class twice.
- A booking is blocked if class capacity is already full.

## Suggested Git Commit Plan
1. Initial project setup
2. Add database models and schema
3. Add member and trainer CRUD
4. Add class, booking, and payment features
5. Add dashboard and documentation

## Deliverables Included
- source code
- final SQL schema
- README
- normalization report
- AI disclosure log
- `.gitignore`

