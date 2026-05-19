USE RetailDW;
GO

IF OBJECT_ID('dbo.ETL_Watermark', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.ETL_Watermark (
        ProcessName VARCHAR(100) PRIMARY KEY,
        LastLoadDate DATETIME NULL,
        UpdatedDate DATETIME DEFAULT GETDATE()
    );
END
GO

IF NOT EXISTS (
    SELECT 1 
    FROM dbo.ETL_Watermark 
    WHERE ProcessName = 'Retail Sales ETL'
)
BEGIN
    INSERT INTO dbo.ETL_Watermark (ProcessName, LastLoadDate)
    VALUES ('Retail Sales ETL', '1900-01-01');
END
GO

SELECT * FROM dbo.ETL_Watermark;