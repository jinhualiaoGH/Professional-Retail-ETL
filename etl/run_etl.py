from db_connection import get_connection
from extract import extract_from_api
from transform import transform_sales_data
from load import (
    load_staging,
    load_dimensions,
    load_fact_sales,
    update_watermark,
    load_error_quarantine
)
from logger_config import setup_logger

logger = setup_logger()

CSV_FILE = "data/sales_orders.csv"


def validate_results(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM StagingSales")
    staging_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM FactSales")
    fact_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(TotalAmount) FROM FactSales")
    total_sales = cursor.fetchone()[0]

    logger.info(f"Staging rows: {staging_count}")
    logger.info(f"Fact rows: {fact_count}")
    logger.info(f"Total sales amount: {total_sales}")


def main():
    conn = get_connection()

    try:
        logger.info("Step 1: Extracting API data...")
        df = extract_from_api()

        if df.empty:
            logger.warning("No new data found. ETL skipped.")
            return

        logger.info("Step 2: Transforming data...")
        df, error_df = transform_sales_data(df)

        logger.info("Loading error quarantine...")
        if not error_df.empty:
             load_error_quarantine(conn, error_df)
        else:
            logger.info("No error rows found.")

        logger.info("Step 3: Loading staging...")
        load_staging(conn, df)

        logger.info("Step 4: Loading dimensions...")
        load_dimensions(conn)

        logger.info("Step 5: Loading fact table...")
        load_fact_sales(conn)

        logger.info("Step 6: Updating watermark...")
        update_watermark(conn)

        logger.info("Step 7: Validating...")
        validate_results(conn)

        logger.info("ETL completed successfully.")

    except Exception as e:
        logger.exception(f"ETL failed: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()