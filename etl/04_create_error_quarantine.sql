USE RetailDW;
GO

DROP TABLE IF EXISTS ETL_Error_Quarantine;
GO

CREATE TABLE ETL_Error_Quarantine (
    ErrorID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NULL,
    CustomerName VARCHAR(100) NULL,
    CustomerEmail VARCHAR(150) NULL,
    Phone VARCHAR(30) NULL,
    ProductName VARCHAR(100) NULL,
    Quantity INT NULL,
    UnitPrice DECIMAL(10,2) NULL,
    ErrorMessage VARCHAR(500),
    ErrorTime DATETIME DEFAULT GETDATE()
);
GO