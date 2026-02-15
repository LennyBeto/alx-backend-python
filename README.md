# Python Generators: Streaming SQL Data

## Objective
Build a Python script that:

Connects to a MySQL server 
Creates a database ALX_prodev and a table user_data if they don't exist
Inserts data from a CSV file (user_data.csv)
Prepares for generator-based streaming of rows
This is Project 0 in the advanced Python generators series.

## Project Structure
├── 0-main.py # Test script to drive seeding logic 
├── seed.py # Main logic for DB creation and data seeding 
├── user_data.csv # Input data (name, email, age) 
└── README.md # This documentation

## Setup Instructions
Install MySQL if not already installed.

Install Python MySQL Connector:

pip install mysql-connector-python
Update seed.py Credentials: Modify:
user="root",
password="your_password"
to match your local MySQL configuration.

Prepare user_data.csv:
Ensure it follows this format:

name,email,age
Alice Smith,alice@example.com,28
Bob Johnson,bob@example.com,32
Run Main Script:
chmod +x seed.py
./seed.py
You should see:

connection successful
Table user_data created successfully
Database ALX_prodev is present
[('uuid1', 'Alice Smith', 'alice@example.com', 28), ...]
🧪 Functions Overview
connect_db() Connects to the MySQL server (no database selected).

create_database(connection) Creates the ALX_prodev database if not present.

connect_to_prodev() Connects to the ALX_prodev database.

create_table(connection) Creates user_data table if it doesn’t exist.

insert_data(connection, data) Inserts rows from CSV into the table (avoids duplicates).

🔁 Task 1: Stream Users with Python Generators
📌 Objective
Create a Python generator that streams rows from a MySQL database table (user_data) one by one using the yield keyword. This promotes memory efficiency and lazy data processing.

📁 File Structure
. ├── 0-stream_users.py # Contains the stream_users generator function ├── seed.py # Sets up the database and inserts data ├── user_data.csv # CSV file used to seed data └── 0-main.py # (Optional) Script to test the generator

🚀 Function Prototype
def stream_users():
    ```
    """Generator that yields user_data rows from MySQL one at a time"""
