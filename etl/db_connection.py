import os
import pyodbc
from dotenv import load_dotenv

load_dotenv("config/.env")

def get_connection():
    server = os.getenv("SERVER")
    database = os.getenv("DATABASE")
    driver = os.getenv("DRIVER")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes;"
    )

    return pyodbc.connect(conn_str)