import logging
import json
import azure.functions as func
import azure.durable_functions as df

# This function is the client function, triggered by a blob upload.
# It starts the Durable Functions orchestration.
def main(inputBlob: func.InputStream, starter: str) -> None:
    logging.info(f"Python blob trigger function processed blob\n"
                 f"Name: {inputBlob.name}\n"
                 f"Size: {inputBlob.length} Bytes")

    # Extract the file name from the blob path
    # Example path: images-input/myimage.jpg
    file_name = inputBlob.name.split('/')[-1]

    # Prepare input for the orchestrator function
    # We pass the blob URI and file name so the orchestrator can access the image
    orchestration_input = {
        "blob_uri": inputBlob.uri,
        "file_name": file_name
    }

    # Get the orchestration client
    client = df.DurableOrchestrationClient(starter)

    # Start the orchestrator function and pass the input
    instance_id = await client.start_new("ImageOrchestrator", None, orchestration_input)

    logging.info(f"Started orchestration with ID = '{instance_id}'.")

    #return f"Orchestration started for {file_name} with ID: {instance_id}"

