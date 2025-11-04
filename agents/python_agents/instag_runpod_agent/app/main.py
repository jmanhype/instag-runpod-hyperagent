"""InsTaG RunPod Agent main application module.

This module provides the FastAPI application for automating InsTaG workflows
on RunPod within the Hypergraph Agents framework.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Placeholder for operator imports, will be added as they are developed
# from . import runpod_ops
# from . import instag_ops

app = FastAPI(
    title="InsTaG RunPod Agent",
    description="Python agent for automating InsTaG on RunPod within the Hypergraph Agents framework.",
    version="0.1.0",
)


@app.post("/api/a2a")
async def handle_a2a_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """Handle incoming A2A messages from the Elixir XCS.

    Args:
        message: A2A protocol message containing type, payload, and metadata.

    Returns:
        A2A protocol response with task results or error information.

    Raises:
        HTTPException: If message validation fails or critical errors occur.
    """
    try:
        # Validate message structure
        if not isinstance(message, dict):
            logger.error("Invalid message format: expected dictionary")
            return JSONResponse(
                {"type": "task_response", "status": "error", "error": "Invalid message format"},
                status_code=400
            )

        message_type: Optional[str] = message.get("type")
        if not message_type or not isinstance(message_type, str):
            logger.error("Missing or invalid 'type' field in message")
            return JSONResponse(
                {"type": "task_response", "status": "error", "error": "Missing or invalid 'type' field"},
                status_code=400
            )

        payload: Dict[str, Any] = message.get("payload", {})
        task_id: str = payload.get("task_id", "unknown_task")

        logger.info(f"Received A2A message: Type={message_type}, TaskID={task_id}, Payload={payload}")

        if message_type == "task_request":
            operation: Optional[str] = payload.get("operation")
            params: Dict[str, Any] = payload.get("params", {})

            # Validate operation field
            if not operation:
                logger.warning(f"Task {task_id}: Missing 'operation' field")
                return {"type": "task_response", "task_id": task_id, "status": "error", "error": "Missing 'operation' field"}

            # Dispatch to appropriate operator based on 'operation'
            # This will be expanded as operators are implemented
            try:
                if operation == "provision_pod":
                    # result = await runpod_ops.provision_pod_op(params)
                    # For now, placeholder:
                    pod_name = params.get('pod_name', 'unnamed_pod')
                    result = {
                        "status": "success",
                        "message": f"Pod provisioning for {pod_name} initiated.",
                        "pod_id": "temp_pod_id_123"
                    }
                    return {"type": "task_response", "task_id": task_id, "status": "completed", "result": result}

                elif operation == "terminate_pod":
                    # result = await runpod_ops.terminate_pod_op(params)
                    # For now, placeholder:
                    pod_id = params.get('pod_id', 'unknown_pod')
                    result = {"status": "success", "message": f"Pod termination for {pod_id} initiated."}
                    return {"type": "task_response", "task_id": task_id, "status": "completed", "result": result}

                elif operation == "instag_setup_environment":
                    # result = await instag_ops.setup_environment_op(params)
                    # For now, placeholder:
                    pod_id = params.get('pod_id', 'unknown_pod')
                    result = {"status": "success", "message": f"InsTaG environment setup for pod {pod_id} initiated."}
                    return {"type": "task_response", "task_id": task_id, "status": "completed", "result": result}

                # Add more operations as they are developed
                else:
                    logger.warning(f"Task {task_id}: Unknown operation '{operation}'")
                    return {"type": "task_response", "task_id": task_id, "status": "error", "error": f"Unknown operation: {operation}"}

            except Exception as op_error:
                logger.error(f"Task {task_id}: Operation '{operation}' failed: {str(op_error)}")
                return {"type": "task_response", "task_id": task_id, "status": "error", "error": f"Operation failed: {str(op_error)}"}

        elif message_type == "agent_discovery_request":
            # Respond with agent card information
            # This should ideally be loaded from a config or the README's agent_card.json example
            agent_card: Dict[str, Any] = {
                "id": "instag_runpod_agent",
                "name": "InsTaG RunPod Agent",
                "version": "0.1.0",
                "description": "Python agent for automating InsTaG on RunPod.",
                "capabilities": [
                    "runpod_provision",
                    "runpod_terminate",
                    "instag_setup_environment",
                    "instag_prepare_data",
                    "instag_run_training",
                    "instag_run_inference"
                ],
                "endpoints": {"a2a": "/api/a2a"}  # Assuming agent_card endpoint is handled by Elixir layer
            }
            return {"type": "agent_discovery_response", "task_id": task_id, "agent_card": agent_card}

        else:
            logger.warning(f"Task {task_id}: Unsupported message type '{message_type}'")
            return {"type": "task_response", "task_id": task_id, "status": "error", "error": f"Unsupported message type: {message_type}"}

    except Exception as e:
        logger.error(f"Unexpected error handling A2A message: {str(e)}", exc_info=True)
        return JSONResponse(
            {"type": "task_response", "status": "error", "error": f"Internal server error: {str(e)}"},
            status_code=500
        )

@app.get("/")
async def read_root() -> Dict[str, str]:
    """Root endpoint providing agent information.

    Returns:
        Dictionary with welcome message and usage instructions.
    """
    return {"message": "Welcome to the InsTaG RunPod Agent. Use the /api/a2a endpoint for A2A communication."}

# Placeholder: In a real scenario, these would be in separate operator files (e.g., runpod_ops.py, instag_ops.py)
# and imported. For now, defining simple placeholders if needed for basic structure.

# async def provision_pod_op(params: dict):
#     print(f"Operator: Provisioning pod with params: {params}")
#     # Actual RunPod API call would go here
#     return {"status": "success", "pod_id": "mock_pod_123", "details": params}

# async def terminate_pod_op(params: dict):
#     print(f"Operator: Terminating pod with params: {params}")
#     # Actual RunPod API call would go here
#     return {"status": "success", "message": f"Pod {params.get('pod_id')} terminated."}

# async def setup_environment_op(params: dict):
#     print(f"Operator: Setting up InsTaG environment with params: {params}")
#     # Actual SSH commands and setup logic would go here
#     return {"status": "success", "message": f"Environment setup on pod {params.get('pod_id')} complete."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002) # Port can be configured

