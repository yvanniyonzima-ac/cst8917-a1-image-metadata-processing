import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()

    metadata = yield context.call_activity("ExtractMetadata", input_data)
    if metadata.get("error"):
        return {
            "status": "failed",
            "step": "ExtractMetadata",
            "message": metadata["message"],
            "trace": metadata.get("trace")
        }

    store_result = yield context.call_activity("StoreMetadata", metadata)
    if store_result.get("error"):
        return {
            "status": "failed",
            "step": "StoreMetadata",
            "message": store_result["message"],
            "trace": store_result.get("trace")
        }

    return {
        "status": "success",
        "metadata": metadata
    }

main = df.Orchestrator.create(orchestrator_function)
