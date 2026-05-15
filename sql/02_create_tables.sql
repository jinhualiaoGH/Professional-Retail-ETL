USE RetailDW;
GO

DROP TABLE IF EXISTS FactSales;
DROP TABLE IF EXISTS DimCustomer;
DROP TABLE IF EXISTS DimProduct;
DROP TABLE IF EXISTS DimRegion;
DROP TABLE IF EXISTS StagingSales;
DROP TABLE IF EXISTS ETL_Log;
GO

CREATE TABLE StagingSales (
    OrderID INT,
    OrderDate DATE,
    CustomerName VARCHAR(100),
    CustomerEmail VARCHAR(150),
    Phone VARCHAR(30),
    ProductName VARCHAR(100),
    Category VARCHAR(100),
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    Region VARCHAR(50),
    SalesRep VARCHAR(100)
);

CREATE TABLE DimCustomer (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerName VARCHAR(100),
    CustomerEmail VARCHAR(150),
    Phone VARCHAR(30),
    CreatedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE DimProduct (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    ProductName VARCHAR(100),
    Category VARCHAR(100),
    UnitPrice DECIMAL(10,2),
    CreatedDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE DimRegion (
    RegionID INT IDENTITY(1,1) PRIMARY KEY,
    Region VARCHAR(50)
);

CREATE TABLE FactSales (
    SalesID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT,
    OrderDate DATE,
    CustomerID INT,
    ProductID INT,
    RegionID INT,
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    TotalAmount DECIMAL(12,2),
    SalesRep VARCHAR(100),
    LoadDate DATETIME DEFAULT GETDATE()
);

CREATE TABLE ETL_Log (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    ProcessName VARCHAR(100),
    Status VARCHAR(20),
    Message VARCHAR(MAX),
    RunDate DATETIME DEFAULT GETDATE()
);