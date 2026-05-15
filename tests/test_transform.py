import sys
import os
import pandas as pd

sys.path.append(os.path.abspath("."))

from etl.transform import transform_sales_data


def test_transform_sales_data():
    data = {
        "OrderID": [1],
        "OrderDate": ["2026-01-01"],
        "CustomerName": [" John Smith "],
        "CustomerEmail": [" JOHN@EMAIL.COM "],
        "Phone": ["7031112222"],
        "ProductName": [" Laptop "],
        "Category": [" Electronics "],
        "Quantity": [2],
        "UnitPrice": [1000],
        "Region": [" East "],
        "SalesRep": ["Alice"]
    }

    df = pd.DataFrame(data)

    result = transform_sales_data(df)

    assert result.iloc[0]["CustomerName"] == "John Smith"
    assert result.iloc[0]["CustomerEmail"] == "john@email.com"
    assert result.iloc[0]["TotalAmount"] == 2000