from retry_utils import retry
import requests
import pandas as pd
from datetime import datetime

API_URL = "https://jsonplaceholder.typicode.com/users"

@retry(max_attempts=3, delay_seconds=5)
def extract_from_api():
    print("Extracting data from REST API...")

    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    users = response.json()

    rows = []

    for user in users:
        rows.append({
            "OrderID": user["id"],
            "OrderDate": datetime.now().date(),
            "CustomerName": user["name"],
            "CustomerEmail": user["email"],
            "Phone": user["phone"],
            "ProductName": "Laptop",
            "Category": "Electronics",
            "Region": "Online",
            "Quantity": 1,
            "UnitPrice": 1200,
            "SalesRep": "API-System"
        })

    df = pd.DataFrame(rows)

    print(f"Rows extracted from API: {len(df)}")
    print(df.columns)

    return df