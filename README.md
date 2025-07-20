# CST8917 Assignment 1: Azure Durable Workflow for Image Metadata Processing

This repository contains the source code for a serverless image metadata processing pipeline built using Azure Durable Functions in Python. This project simulates a real-world event-driven system where user-uploaded images are automatically processed to extract and store their metadata.

## Objective

The primary objective of this project is to demonstrate the use of Azure Durable Functions, including blob triggers, orchestrator functions, activity functions, and interaction with Azure SQL Database, to create a robust and scalable image metadata processing workflow.

## Scenario

A fictional content moderation team requires an automated solution to analyze the metadata of user-uploaded images. This Azure Durable Functions application fulfills this requirement by:
* Automatically triggering when a new image is uploaded to Azure Blob Storage.
* Extracting key metadata (e.g., file size, format, dimensions).
* Storing the extracted metadata in an Azure SQL Database for further analysis.

## Workflow Requirements

The Durable Functions application implements the following multi-step workflow:

### Step 1: Blob Trigger (Client Function) - `ImageUploadTrigger`

* **Purpose:** Initiates the entire workflow.
* **Trigger:** Automatically activated when a new image (`.jpg`, `.png`, or `.gif`) is uploaded to a specific Azure Blob Storage container (e.g., `images-input`).
* **Action:** Acts as the client function for Durable Functions. It extracts the blob URI and file name of the uploaded image and starts a new instance of the `ImageOrchestrator` function, passing the image details as input.

### Step 2: Orchestrator Function - `ImageOrchestrator`

* **Purpose:** Coordinates the execution of the activity functions.
* **Action:**
    1.  Receives the blob URI and file name from the `ImageUploadTrigger`.
    2.  Calls the `ExtractImageMetadata` activity function to get the image's metadata.
    3.  Once metadata is extracted, it calls the `StoreImageMetadata` activity function to persist this data in Azure SQL Database.
    4.  Manages the state and progress of the entire image processing operation.

### Step 3: Activity Function – Extract Metadata - `ExtractImageMetadata`

* **Purpose:** Extracts specific metadata from the image.
* **Input:** Blob URI and file name of the uploaded image.
* **Action:**
    1.  Downloads the image content from the provided blob URI.
    2.  Uses the `Pillow` (PIL) library to open and process the image.
    3.  Extracts the following metadata:
        * File name
        * File size (in KB)
        * Width and height (in pixels)
        * Image format (e.g., JPEG, PNG, GIF)
    4.  Returns the extracted metadata as a dictionary.

### Step 4: Activity Function – Store Metadata - `StoreImageMetadata`

* **Purpose:** Stores the extracted image metadata in Azure SQL Database.
* **Input:** The metadata dictionary returned by `ExtractImageMetadata`.
* **Action:**
    1.  Connects to an Azure SQL Database using a connection string retrieved from the Function App's application settings (`SqlConnectionString`).
    2.  Inserts the extracted metadata (File Name, File Size, Width, Height, Image Format) into a pre-defined `ImageMetadata` table in the SQL Database.
    3.  Utilizes `pyodbc` for database interaction.

## Project Structure


.
├── host.json
├── requirements.txt
├── ImageUploadTrigger/
│   ├── function.json
│   └── init.py
├── ImageOrchestrator/
│   ├── function.json
│   └── init.py
├── ExtractImageMetadata/
│   ├── function.json
│   └── init.py
└── StoreImageMetadata/
├── function.json
└── init.py


## Setup and Deployment

1.  **Azure Resources:**
    * **Azure Function App:** Deploy this project to an Azure Function App (Python runtime).
    * **Azure Storage Account:** Create a blob container named `images-input` in your storage account. This is where images will be uploaded.
    * **Azure SQL Database:** Create an Azure SQL Database and a table named `ImageMetadata` with appropriate columns (e.g., `FileName NVARCHAR(255)`, `FileSizeKB DECIMAL(10,2)`, `Width INT`, `Height INT`, `ImageFormat NVARCHAR(50)`, `ProcessedDate DATETIME DEFAULT GETDATE()`). Ensure firewall rules allow access from your Function App.

2.  **Application Settings:**
    * In your Azure Function App's configuration, add an application setting named `SqlConnectionString` with the connection string to your Azure SQL Database.
    * Ensure `AzureWebJobsStorage` is set to your storage account connection string.

3.  **Deployment:**
    * Push this code to a GitHub repository.
    * Set up Continuous Deployment from your GitHub repository to your Azure Function App using GitHub Actions via the Azure portal's Deployment Center. Ensure your GitHub Actions workflow specifies a compatible Python version (e.g., `3.9` or `3.10`) and updates `pip` before installing dependencies.

## How to Test

1.  **Upload an Image:** Upload a `.jpg`, `.png`, or `.gif` image file to the `images-input` blob container in your Azure Storage Account.
2.  **Monitor:**
    * Check the "Monitor" section or "Log stream" of your `ImageUploadTrigger` and `ImageOrchestrator` functions in the Azure portal for execution logs.
    * Verify that the metadata has been inserted into your `ImageMetadata` table in Azure SQL Database.

## YouTube Demo

A video demonstration of this Azure Durable Functions workflow in action can be found here:

[**Link to your YouTube Demo Video**](https://youtu.be/rPoW8IO72BY)



**Note:** This project is for educational purposes (CST8917 Assignment 1) and demonstrates core concepts of Azure Durable Functions.
