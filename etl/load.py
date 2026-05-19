import pandas as pd


def load_staging(conn, df):
    cursor = conn.cursor()

    # clear staging first
    cursor.execute("TRUNCATE TABLE StagingSales")

    insert_sql = """
    INSERT INTO StagingSales (
        OrderID,
        OrderDate,
        CustomerName,
        CustomerEmail,
        Phone,
        ProductName,
        Category,
        Region,
        Quantity,
        UnitPrice,
        SalesRep
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    for _, row in df.iterrows():
        cursor.execute(
            insert_sql,
            row["OrderID"],
            row["OrderDate"],
            row["CustomerName"],
            row["CustomerEmail"],
            row["Phone"],
            row["ProductName"],
            row["Category"],
            row["Region"],
            row["Quantity"],
            row["UnitPrice"],
            row["SalesRep"]
        )

    conn.commit()


def load_dimensions(conn):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO DimCustomer (CustomerName, CustomerEmail, Phone)
        SELECT DISTINCT CustomerName, CustomerEmail, Phone
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1 FROM DimCustomer d
            WHERE d.CustomerEmail = s.CustomerEmail
        )
    """)

    cursor.execute("""
        INSERT INTO DimProduct (ProductName, Category)
        SELECT DISTINCT ProductName, Category
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1 FROM DimProduct d
            WHERE d.ProductName = s.ProductName
        )
    """)

    cursor.execute("""
        INSERT INTO DimRegion (Region, SalesRep)
        SELECT DISTINCT Region, SalesRep
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1 FROM DimRegion d
            WHERE d.Region = s.Region
        )
    """)

    conn.commit()

def load_fact_sales(conn):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO FactSales
        (OrderID, OrderDate, CustomerID, ProductID, RegionID,
         Quantity, UnitPrice, TotalAmount, SalesRep)
        SELECT
            s.OrderID,
            s.OrderDate,
            c.CustomerID,
            p.ProductID,
            r.RegionID,
            s.Quantity,
            s.UnitPrice,
            s.Quantity * s.UnitPrice,
            s.SalesRep
        FROM StagingSales s
        JOIN DimCustomer c
            ON s.CustomerEmail = c.CustomerEmail
        JOIN DimProduct p
            ON s.ProductName = p.ProductName
           AND s.Category = p.Category
        JOIN DimRegion r
            ON s.Region = r.Region
        WHERE NOT EXISTS (
            SELECT 1
            FROM FactSales f
            WHERE f.OrderID = s.OrderID
        )
    """)

    conn.commit()


def update_watermark(conn):
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE dbo.ETL_Watermark
        SET LastLoadDate = (
            SELECT MAX(OrderDate)
            FROM dbo.StagingSales
        ),
        UpdatedDate = GETDATE()
        WHERE ProcessName = 'Retail Sales ETL'
    """)

    conn.commit()
    print("Watermark updated.")


def load_error_quarantine(conn, error_df):
    if error_df.empty:
        print("No error rows found.")
        return

    cursor = conn.cursor()

    for _, row in error_df.iterrows():
        cursor.execute("""
            INSERT INTO ETL_Error_Quarantine
            (OrderID, CustomerName, CustomerEmail, Phone,
             ProductName, Quantity, UnitPrice, ErrorMessage)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        None if pd.isna(row.get("OrderID")) else int(row.get("OrderID")),
        row.get("CustomerName"),
        row.get("CustomerEmail"),
        row.get("Phone"),
        row.get("ProductName"),
        None if pd.isna(row.get("Quantity")) else int(row.get("Quantity")),
        None if pd.isna(row.get("UnitPrice")) else float(row.get("UnitPrice")),
        row.get("ErrorMessage")
        )

    conn.commit()
    print(f"Error rows quarantined: {len(error_df)}")