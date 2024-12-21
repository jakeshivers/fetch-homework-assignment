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
    DECIMAL,
    TIMESTAMP,
    MetaData,
    ForeignKey,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import URL
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection parameters
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
BRANDS_FILE = os.environ.get("BRANDS_FILE")

logger.info(f"DB_USER: {DB_USER}")
logger.info(f"BRANDS_FILE: {BRANDS_FILE}")
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
logger.info(f"Database engine created: {engine}")

# Define SQLAlchemy metadata and table schemas
metadata = MetaData()

brands = Table(
    "brands",
    metadata,
    Column("brand_id", String(24), primary_key=True),
    Column("ref", String(24), nullable=True),
    Column("barcode", String, default=""),
    Column("brand_code", String, default=""),
    Column("category", String, default="UNKNOWN"),
    Column("category_code", String, default="UNKNOWN"),
    Column("top_brand", Boolean, default=False),
    Column("name", String, default="UNKNOWN"),
)

cpg = Table(
    "cpg",
    metadata,
    Column("cpg_id", String(24), primary_key=True),
    Column("ref", String, default="UNKNOWN"),
)


# Helper function to parse boolean values
def parse_boolean(value):
    """Convert various representations of boolean values to True or False."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ["true", "1", "yes"]
    if isinstance(value, int):
        return value == 1
    return False  # Default to False for invalid values


# Function to load brands and CPG data into the database
def load_brands(BRANDS_FILE):
    if not os.path.exists(BRANDS_FILE):
        logger.error(f"File not found: {BRANDS_FILE}")
        return

    with engine.connect() as connection:
        with open(BRANDS_FILE, "r") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # Log raw line for debugging
                    logger.info(f"Processing line {line_number}: {line.strip()}")

                    # Parse the JSON object
                    record = json.loads(line.strip())

                    # Extract CPG data
                    cpg_data = {
                        "cpg_id": record.get("cpg", {})
                        .get("$id", {})
                        .get("$oid", f"unknown_cpg_{line_number}"),
                        "ref": record.get("cpg", {}).get("$ref", "UNKNOWN"),
                    }
                    logger.debug(f"Parsed CPG data: {cpg_data}")

                    # Insert CPG data
                    try:
                        with connection.begin():  # Explicit transaction for CPG
                            connection.execute(cpg.insert().values(cpg_data))
                            logger.info(f"Inserted CPG for line {line_number}")
                    except IntegrityError:
                        logger.warning(f"CPG already exists: {cpg_data['cpg_id']}")

                    # Extract brand-level data
                    brand_data = {
                        "brand_id": record.get("_id", {}).get(
                            "$oid", f"unknown_brand_{line_number}"
                        ),
                        "ref": record.get("cpg", {}).get("$id", {}).get("$oid", None),
                        "barcode": record.get("barcode", ""),
                        "brand_code": record.get("brandCode", ""),
                        "category": record.get("category", "UNKNOWN"),
                        "category_code": record.get("categoryCode", "UNKNOWN"),
                        "top_brand": parse_boolean(record.get("topBrand", False)),
                        "name": record.get("name", "UNKNOWN"),
                    }
                    logger.debug(f"Parsed brand data: {brand_data}")

                    # Insert brand data
                    try:
                        with connection.begin():  # Explicit transaction for Brand
                            connection.execute(brands.insert().values(brand_data))
                            logger.info(f"Inserted brand for line {line_number}")
                    except IntegrityError:
                        logger.warning(
                            f"Brand already exists: {brand_data['brand_id']}"
                        )

                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error on line {line_number}: {e}")
                except Exception as e:
                    logger.error(f"Error processing line {line_number}: {e}")
                    connection.rollback()  # Rollback on generic error to prevent blockages


# Main function
def main():
    load_brands(BRANDS_FILE)
    logger.info("Data loading complete.")


if __name__ == "__main__":
    main()
