# InsTaG RunPod Agent

This Python agent is designed to automate the InsTaG (Implicit Suffix Tree Graph) workflow on RunPod, as part of the `hypergraph_agents_umbrella` framework.

## Features
- Interacts with the RunPod API to provision, manage, and terminate pods.
- Sets up the environment within RunPod pods (cloning repositories, Conda environments, installing dependencies).
- Manages data download and preparation for InsTaG (e.g., BFM model, training datasets).
- Orchestrates the execution of InsTaG training and inference scripts.
- Communicates with the Elixir orchestration layer (XCS) via the A2A protocol.

## Tech Stack
- Python 3.9+
- FastAPI (async HTTP, OpenAPI docs)
- Uvicorn (ASGI server)
- RunPod SDK (`runpod`)
- Paramiko (for SSH)
- Requests (for HTTP calls)

## Usage

### 1. Install dependencies
```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the agent
```sh
uvicorn app.main:app --reload --port 5002 # Or another available port
```

### 3. Agent Registration & Interaction
This agent will register with the Elixir A2A system. The Elixir XCS will then send `task_request` messages to this agent's `/api/a2a` endpoint to trigger specific InsTaG operations.

## Agent Card Example (to be adapted)
```json
{
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
  "endpoints": {"a2a": "/api/a2a", "agent_card": "/api/agent_card"},
  "authentication": null
}
```

## License
MIT

