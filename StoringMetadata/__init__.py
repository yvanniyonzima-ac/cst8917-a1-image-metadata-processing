import logging
import os
import pyodbc
import json

# This activity function stores the extracted image metadata into an Azure SQL Database.
def main(metadata: dict):
    logging.info(f"StoreImageMetadata activity function started. Metadata to store: {metadata}")

    # Retrieve the SQL connection string from application settings.
    # In Azure, this would be set as an Application Setting (e.g., in Configuration -> Application settings).
    # Locally, you can set it in local.settings.json.
    sql_connection_string = os.environ.get("SqlConnectionString")

    if not sql_connection_string:
        logging.error("SqlConnectionString environment variable not set.")
        raise ValueError("Azure SQL Database connection string is missing.")

    try:
        # Establish a connection to Azure SQL Database
        # Ensure your SQL server allows connections from Azure Functions (firewall rules)
        cnxn = pyodbc.connect(sql_connection_string)
        cursor = cnxn.cursor()

        # Define the SQL table schema.
        # You should create this table in your Azure SQL Database beforehand.
        # Example SQL to create the table:
        # CREATE TABLE ImageMetadata (
        #     Id INT IDENTITY(1,1) PRIMARY KEY,
        #     FileName NVARCHAR(255) NOT NULL,
        #     FileSizeKB DECIMAL(10, 2),
        #     Width INT,
        #     Height INT,
        #     ImageFormat NVARCHAR(50),
        #     ProcessedDate DATETIME DEFAULT GETDATE()
        # );

        # Prepare the SQL INSERT statement
        insert_sql = """
        INSERT INTO ImageMetadata (FileName, FileSizeKB, Width, Height, ImageFormat)
        VALUES (?, ?, ?, ?, ?)
        """
        # Extract data from the metadata dictionary
        file_name = metadata.get("FileName")
        file_size_kb = metadata.get("FileSizeKB")
        width = metadata.get("Width")
        height = metadata.get("Height")
        image_format = metadata.get("ImageFormat")

        # Execute the INSERT statement
        cursor.execute(insert_sql, file_name, file_size_kb, width, height, image_format)

        # Commit the transaction
        cnxn.commit()
        logging.info(f"Successfully stored metadata for {file_name} in Azure SQL DB.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        logging.error(f"Database error occurred: {sqlstate} - {ex}")
        # Rollback in case of error
        if cnxn:
            cnxn.rollback()
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during storing metadata: {e}")
        raise
    finally:
        # Close the connection
        if cnxn:
            cnxn.close()

