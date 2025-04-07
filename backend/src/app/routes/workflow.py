from uuid import uuid4
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.system.WorkflowSystem import WorkflowSystem

router = APIRouter()
workflow_instances: Dict[str, WorkflowSystem] = {}

# Pydantic models
class InitWorkflowRequest(BaseModel):
    config: Dict[str, Any]

class InitWorkflowResponse(BaseModel):
    workflow_id: str
    message: str

@router.post("/init", response_model=InitWorkflowResponse)
async def init_workflow(request: InitWorkflowRequest):
    system = WorkflowSystem(config=request.config)
    workflow_id = str(uuid4())
    workflow_instances[workflow_id] = system

    return InitWorkflowResponse(
        workflow_id=workflow_id,
        message=f"Workflow {workflow_id} initialized successfully."
    )

@router.get("/list")
async def list_workflows() -> Dict[str, str]:
    return {wid: "WorkflowSystem instance" for wid in workflow_instances}

# Helper function to access from chat_routes
def get_workflow(workflow_id: str) -> WorkflowSystem:
    if workflow_id not in workflow_instances:
        raise HTTPException(status_code=404, detail="Workflow ID not found")
    return workflow_instances[workflow_id]
