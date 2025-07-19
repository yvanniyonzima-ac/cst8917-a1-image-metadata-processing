import logging
import azure.durable_functions as df

# This is the orchestrator function. It defines the workflow
# by calling activity functions in a specific order.
def orchestrator_function(context: df.DurableOrchestrationContext):
    logging.info("Orchestrator function started.")

    # Get the input from the client function (blob trigger)
    # This input contains the blob_uri and file_name
    orchestration_input = context.get_input()
    blob_uri = orchestration_input["blob_uri"]
    file_name = orchestration_input["file_name"]

    logging.info(f"Orchestrating processing for file: {file_name} from URI: {blob_uri}")

    try:
        # Step 1: Call the activity function to extract metadata
        # Pass the blob_uri and file_name to the activity function
        metadata = yield context.call_activity("ExtractImageMetadata", {
            "blob_uri": blob_uri,
            "file_name": file_name
        })
        logging.info(f"Extracted metadata: {metadata}")

        # Step 2: Call the activity function to store the metadata in Azure SQL DB
        # Pass the extracted metadata to the activity function
        yield context.call_activity("StoreImageMetadata", metadata)
        logging.info(f"Stored metadata for {file_name} in Azure SQL DB.")

        return f"Image metadata processing completed for {file_name}."

    except Exception as e:
        logging.error(f"Error during orchestration for {file_name}: {e}")
        # You can add error handling logic here, e.g., send a notification
        return f"Image metadata processing failed for {file_name}: {e}"

main = df.Orchestrator.create(orchestrator_function)
