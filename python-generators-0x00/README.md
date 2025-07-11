# Python Generators

### This directory is all about Python generators and their practical uses.  
Here, you'll find projects and exercises demonstrating how to leverage generators for efficient data handling. 
Learn to stream large datasets directly from a database and implement lazy pagination, which is perfect for working 
with massive amounts of information without consuming excessive memory.

# Topics Covered
## Python Generators: Efficient Data Handling
This directory showcases the power of Python generators for efficient data streaming and memory management. 
You'll find practical examples covering:

- Creating and using generator functions
- Streaming database records efficiently
- Lazy evaluation and memory efficiency
- Implementing pagination with generators

## Files
- 0-stream_users.py: A generator that efficiently streams user records one at a time from a MySQL database.
- 1-main.py: Demonstrates example usage of the user streaming generator.
- 2-lazy_paginate.py: Implements lazy pagination to fetch user data in optimized batches.
- 4-stream-ages.py: A generator specifically designed to stream only user ages from the database.
- seed.py: Contains utility functions for database connection, table setup, and initial data seeding.

## Usage
To run any of the example scripts, use:
- Bash
  python3 <script_name.py>

### Example
- Bash
  python3 1-main.py

### Requirements
- Python 3.x
- mysql-connector-python
- python-dotenv
- A running MySQL server with the necessary database and table configured.
