import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()
    metadata = yield context.call_activity("ExtractMetadata", input_data)
    yield context.call_activity("StoreMetadata", metadata)
    return metadata

main = df.Orchestrator.create(orchestrator_function)
