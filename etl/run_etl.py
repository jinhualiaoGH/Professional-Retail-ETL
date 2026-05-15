from db_connection import get_connection
from extract import extract_csv
from transform import transform_sales_data
from load import load_staging, load_dimensions, load_fact_sales, log_message

CSV_FILE = "data/sales_orders.csv"


def validate_results(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM StagingSales")
    staging_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM FactSales")
    fact_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(TotalAmount) FROM FactSales")
    total_sales = cursor.fetchone()[0]

    print(f"Staging rows: {staging_count}")
    print(f"Fact rows: {fact_count}")
    print(f"Total sales amount: {total_sales}")


def main():
    conn = None

    try:
        print("Starting Retail Sales ETL...")

        conn = get_connection()

        log_message(conn, "Retail Sales ETL", "STARTED", "ETL process started")

        print("Step 1: Extracting CSV...")
        df = extract_csv(CSV_FILE)

        print("Step 2: Transforming data...")
        df = transform_sales_data(df)

        print("Step 3: Loading staging...")
        load_staging(conn, df)

        print("Step 4: Loading dimensions...")
        load_dimensions(conn)

        print("Step 5: Loading fact table...")
        load_fact_sales(conn)

        print("Step 6: Validating...")
        validate_results(conn)

        log_message(conn, "Retail Sales ETL", "SUCCESS", "ETL completed successfully")

        print("ETL completed successfully.")

    except Exception as e:
        print(f"ETL failed: {e}")

        if conn:
            log_message(conn, "Retail Sales ETL", "FAILED", str(e))

    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    main()