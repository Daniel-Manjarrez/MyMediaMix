import sqlite3
import os
import csv

def print_all_entries(cursor):
    cursor.execute("SELECT * FROM movies")
    all_rows = cursor.fetchall()
    print("All movies in the database:")
    for row in all_rows:
        print(row)

def close_database_connection(conn):
    conn.close()
    print("Database connection closed")

def query_database(query, cursor):
    cursor.execute(f"{query}")
    return cursor.fetchall()

def print_query_retrieval(data):
    for item in data:
        print(item)

# Function to create a SQLite database and import data from CSV
def create_sqlite_db(csv_file, db_file):
    # Use os.path to ensure the paths are correct
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, csv_file)
    db_path = os.path.join(base_dir, db_file)
    
    # connect to SQLite database (will create it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if conn is not None and cursor is not None:
        print("Successfully established connection and cursor")
        print(f"Connection at : {conn} \nCursor at: {cursor}")
        print(f"Database created and data imported from {csv_file} to {db_file}")

    cursor.execute("DROP TABLE IF EXISTS movies")

    # create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            watchmode_id INTEGER PRIMARY KEY,
            imdb_id TEXT,
            tmdb_id INTEGER,
            tmdb_type TEXT,
            title TEXT,
            year INTEGER
        )
    ''')

    # read data from CSV and insert into the SQLite table
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row
        for row in reader:
            cursor.execute('''
                INSERT INTO movies (watchmode_id, imdb_id, tmdb_id, tmdb_type, title, year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', row)

    # commit changes
    conn.commit()

    return (conn, cursor)