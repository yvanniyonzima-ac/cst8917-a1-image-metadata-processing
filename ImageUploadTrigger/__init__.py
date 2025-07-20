import azure.functions as func
import azure.durable_functions as df
import logging

def main(inputBlob: func.InputStream, starter: str):
    client = df.DurableOrchestrationClient(starter)
    instance_id = client.start_new("OrchestratorFunction", None, {
        "name": inputBlob.name,
        "blob_url": inputBlob.uri
    })
    logging.info(f"Started orchestration with ID = '{instance_id}'.")
