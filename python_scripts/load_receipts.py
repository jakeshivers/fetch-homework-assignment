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
RECEIPTS_FILE = os.environ.get("RECEIPTS_FILE")

logger.info(f"DB_USER: {DB_USER}")
logger.info(f"RECEIPTS_FILE: {RECEIPTS_FILE}")

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

receipts = Table(
    "receipts",
    metadata,
    Column("receipt_id", String, primary_key=True),
    Column("user_id", String, default="unknown_user"),
    Column("bonus_points_earned", Integer, default=0),
    Column("bonus_points_reason", String, default=""),
    Column("create_date", TIMESTAMP, nullable=True),
    Column("date_scanned", TIMESTAMP, nullable=True),
    Column("finished_date", TIMESTAMP, nullable=True),
    Column("modify_date", TIMESTAMP, nullable=True),
    Column("points_awarded_date", TIMESTAMP, nullable=True),
    Column("points_earned", DECIMAL, default=0.0),
    Column("purchase_date", TIMESTAMP, nullable=True),
    Column("purchase_item_count", Integer, default=0),
    Column("reward_receipt_status", String, default="UNKNOWN"),
    Column("total_spent", DECIMAL, default=0.0),
)

receipt_items = Table(
    "receipt_items",
    metadata,
    Column("item_id", Integer, primary_key=True, autoincrement=True),
    Column("receipt_id", String, ForeignKey("receipts.receipt_id")),
    Column("barcode", String, default=""),
    Column("description", String, default="UNKNOWN"),
    Column("final_price", DECIMAL, default=0.0),
    Column("needs_fetch_review", Boolean, default=False),
    Column("partner_item_id", Boolean, default=False),
    Column("prevent_target_gap_points", Boolean, default=False),
    Column("quantity_purchased", Integer, default=0),
    Column("user_flagged_barcode", String, default=""),
    Column("user_flagged_new_item", Boolean, default=False),
    Column("user_flagged_price", DECIMAL, default=0.0),
    Column("user_flagged_quantity", Integer, default=0),
)


# Helper function to parse dates
def parse_date(date_ms):
    """Convert milliseconds since epoch to a Python datetime."""
    if date_ms:
        try:
            return datetime.fromtimestamp(date_ms / 1000)
        except Exception as e:
            logger.error(f"Failed to parse date: {date_ms} - {e}")
            return None
    return None


# Helper function to parse decimals
def parse_decimal(value):
    """Convert a string or number to a decimal, handling None values gracefully."""
    if value:
        try:
            return float(value)
        except Exception as e:
            logger.error(f"Failed to parse decimal: {value} - {e}")
            return 0.0
    return 0.0


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


# Function to load receipts and items into the database
def load_receipts(RECEIPTS_FILE):
    if not os.path.exists(RECEIPTS_FILE):
        logger.error(f"File not found: {RECEIPTS_FILE}")
        return

    with engine.connect() as connection:
        with open(RECEIPTS_FILE, "r") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    # Log raw line for debugging
                    logger.info(f"Processing line {line_number}: {line.strip()}")

                    # Parse the JSON object
                    record = json.loads(line.strip())

                    # Extract receipt-level data with defaults
                    receipt_data = {
                        "receipt_id": record.get("_id", {}).get(
                            "$oid", f"unknown_{line_number}"
                        ),
                        "user_id": record.get("userId", "unknown_user"),
                        "bonus_points_earned": record.get("bonusPointsEarned", 0),
                        "bonus_points_reason": record.get(
                            "bonusPointsEarnedReason", ""
                        ),
                        "create_date": parse_date(
                            record.get("createDate", {}).get("$date")
                        ),
                        "date_scanned": parse_date(
                            record.get("dateScanned", {}).get("$date")
                        ),
                        "finished_date": parse_date(
                            record.get("finishedDate", {}).get("$date")
                        ),
                        "modify_date": parse_date(
                            record.get("modifyDate", {}).get("$date")
                        ),
                        "points_awarded_date": parse_date(
                            record.get("pointsAwardedDate", {}).get("$date")
                        ),
                        "points_earned": parse_decimal(record.get("pointsEarned", 0)),
                        "purchase_date": parse_date(
                            record.get("purchaseDate", {}).get("$date")
                        ),
                        "purchase_item_count": record.get("purchasedItemCount", 0),
                        "reward_receipt_status": record.get(
                            "rewardsReceiptStatus", "UNKNOWN"
                        ),
                        "total_spent": parse_decimal(record.get("totalSpent", 0)),
                    }
                    logger.debug(f"Parsed receipt data: {receipt_data}")

                    # Insert receipt data
                    try:
                        with connection.begin() as trans:
                            connection.execute(receipts.insert().values(receipt_data))
                            logger.info(f"Inserted receipt for line {line_number}")

                            # Extract and insert item-level data
                            items = record.get("rewardsReceiptItemList", [])
                            for item in items:
                                item_data = {
                                    "receipt_id": receipt_data["receipt_id"],
                                    "barcode": item.get("barcode", ""),
                                    "description": item.get("description", "UNKNOWN"),
                                    "final_price": parse_decimal(
                                        item.get("finalPrice", 0)
                                    ),
                                    "needs_fetch_review": parse_boolean(
                                        item.get("needsFetchReview", False)
                                    ),
                                    "partner_item_id": parse_boolean(
                                        item.get("partnerItemId", False)
                                    ),
                                    "prevent_target_gap_points": parse_boolean(
                                        item.get("preventTargetGapPoints", False)
                                    ),
                                    "quantity_purchased": item.get(
                                        "quantityPurchased", 0
                                    ),
                                    "user_flagged_barcode": item.get(
                                        "userFlaggedBarcode", ""
                                    ),
                                    "user_flagged_new_item": parse_boolean(
                                        item.get("userFlaggedNewItem", False)
                                    ),
                                    "user_flagged_price": parse_decimal(
                                        item.get("userFlaggedPrice", 0)
                                    ),
                                    "user_flagged_quantity": item.get(
                                        "userFlaggedQuantity", 0
                                    ),
                                }
                                connection.execute(
                                    receipt_items.insert().values(item_data)
                                )
                                logger.info(
                                    f"Inserted item for receipt_id: {receipt_data['receipt_id']}"
                                )
                    except IntegrityError as e:
                        logger.error(
                            f"Failed to insert receipt or items for line {line_number}: {e}"
                        )

                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error on line {line_number}: {e}")
                except Exception as e:
                    logger.error(f"Error processing line {line_number}: {e}")


# Main function
def main():
    load_receipts(RECEIPTS_FILE)
    logger.info("Data loading complete.")


if __name__ == "__main__":
    main()
