import pandas as pd

def transform_sales_data(df):
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")

    df["CustomerName"] = df["CustomerName"].str.strip()
    df["CustomerEmail"] = df["CustomerEmail"].str.lower().str.strip()
    df["ProductName"] = df["ProductName"].str.strip()
    df["Category"] = df["Category"].str.strip()
    df["Region"] = df["Region"].str.strip()

    df = df.dropna(subset=["OrderID", "OrderDate", "CustomerName", "ProductName"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    df["TotalAmount"] = df["Quantity"] * df["UnitPrice"]

    return df