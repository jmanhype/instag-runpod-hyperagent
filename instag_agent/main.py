"""InsTaG RunPod Agent - Alternative entry point.

This module provides an alternative FastAPI application entry point for the
InsTaG RunPod Agent. For the main implementation, see agents/python_agents/instag_runpod_agent/.
"""

from fastapi import FastAPI
from typing import Dict

app = FastAPI(
    title="InsTaG RunPod Agent",
    description="Alternative entry point for InsTaG RunPod automation",
    version="0.1.0",
)


@app.get("/")
def read_root() -> Dict[str, str]:
    """Root endpoint providing basic agent information.

    Returns:
        Dictionary with welcome message.
    """
    return {"message": "Welcome to the InsTaG RunPod Agent"}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring and orchestration.

    Returns:
        Dictionary with health status.
    """
    return {"status": "healthy", "service": "instag_runpod_agent"}


# More endpoints will be added here by the agent as it processes the tasks

