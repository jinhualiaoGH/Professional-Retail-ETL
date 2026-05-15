def log_message(conn, process_name, status, message):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ETL_Log (ProcessName, Status, Message)
        VALUES (?, ?, ?)
    """, process_name, status, message)

    conn.commit()


def load_staging(conn, df):
    cursor = conn.cursor()

    cursor.execute("TRUNCATE TABLE StagingSales")

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO StagingSales
            (OrderID, OrderDate, CustomerName, CustomerEmail, Phone,
             ProductName, Category, Quantity, UnitPrice, Region, SalesRep)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        int(row["OrderID"]),
        row["OrderDate"],
        row["CustomerName"],
        row["CustomerEmail"],
        row["Phone"],
        row["ProductName"],
        row["Category"],
        int(row["Quantity"]),
        float(row["UnitPrice"]),
        row["Region"],
        row["SalesRep"]
        )

    conn.commit()


def load_dimensions(conn):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO DimCustomer (CustomerName, CustomerEmail, Phone)
        SELECT DISTINCT s.CustomerName, s.CustomerEmail, s.Phone
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1
            FROM DimCustomer d
            WHERE d.CustomerEmail = s.CustomerEmail
        )
    """)

    cursor.execute("""
        INSERT INTO DimProduct (ProductName, Category, UnitPrice)
        SELECT DISTINCT s.ProductName, s.Category, s.UnitPrice
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1
            FROM DimProduct d
            WHERE d.ProductName = s.ProductName
              AND d.Category = s.Category
        )
    """)

    cursor.execute("""
        INSERT INTO DimRegion (Region)
        SELECT DISTINCT s.Region
        FROM StagingSales s
        WHERE NOT EXISTS (
            SELECT 1
            FROM DimRegion d
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