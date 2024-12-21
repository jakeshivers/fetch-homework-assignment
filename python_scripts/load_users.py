import json
import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import (
    create_engine,
    Table,
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    MetaData,
)
from sqlalchemy.exc import IntegrityError, ProgrammingError
from sqlalchemy.engine import URL
import logging

# Enable SQL logging for debugging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
USERS_FILE = os.getenv("USERS_FILE")

# Define the connection URL
connection_url = URL.create(
    drivername="postgresql+pg8000",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

# Initialize the database engine
engine = create_engine(connection_url)
print(f"Connecting to: {engine}")

# Define the users table
metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("record_id", Integer, primary_key=True, autoincrement=True),  # Surrogate key
    Column("id", String),  # Original ID
    Column("active", Boolean),
    Column("created_date", TIMESTAMP),
    Column("last_login", TIMESTAMP, nullable=True),
    Column("role", String, nullable=True),
    Column("sign_up_source", String, nullable=True),
    Column("state", String, nullable=True),
)

# Create the table if it doesn't exist
metadata.create_all(engine)


# Function to insert users into the database
def insert_users_from_file(file_path):
    with engine.connect() as connection:
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # Parse the JSON object
                    record = json.loads(line.strip())

                    # Extract fields with default values for missing fields
                    user_id = record["_id"]["$oid"]
                    active = record["active"]
                    created_date = datetime.fromtimestamp(
                        record["createdDate"]["$date"] / 1000
                    )
                    last_login = (
                        datetime.fromtimestamp(record["lastLogin"]["$date"] / 1000)
                        if "lastLogin" in record
                        else None
                    )
                    role = record.get("role", None)
                    sign_up_source = record.get("signUpSource", None)
                    state = record.get("state", None)

                    # Insert into the database
                    trans = connection.begin()
                    try:
                        connection.execute(
                            users.insert().values(
                                id=user_id,
                                active=active,
                                created_date=created_date,
                                last_login=last_login,
                                role=role,
                                sign_up_source=sign_up_source,
                                state=state,
                            )
                        )
                        trans.commit()
                        print(f"Inserted record from line {line_number}")
                    except Exception as e:
                        trans.rollback()
                        print(f"Error inserting record from line {line_number}: {e}")

                except json.JSONDecodeError as e:
                    print(f"JSON error on line {line_number}: {e}")
                except Exception as e:
                    print(f"Error processing line {line_number}: {e}")


# Main function
def main():
    print("\nStarting data insertion...")
    try:
        insert_users_from_file(USERS_FILE)
        print("\nAll records processed.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
