import pandas as pd


def transform_sales_data(df):
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

    text_columns = [
        "CustomerName",
        "CustomerEmail",
        "ProductName",
        "Category",
        "Region",
        "SalesRep"
    ]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["CustomerEmail"] = df["CustomerEmail"].str.lower()

    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    valid_rows = df[
        df["OrderID"].notna()
        & df["OrderDate"].notna()
        & df["CustomerName"].notna()
        & df["CustomerEmail"].notna()
        & df["ProductName"].notna()
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    error_rows = df.drop(valid_rows.index).copy()
    error_rows["ErrorMessage"] = "Invalid required field, quantity, price, or date"

    return valid_rows, error_rows