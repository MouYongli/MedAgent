from typing import Dict, Any, Optional
from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.models.system.WorkflowSystem import WorkflowSystem

router = APIRouter()
workflow_instances: Dict[str, WorkflowSystem] = {}


# Pydantic models
class InitWorkflowRequest(BaseModel):
    config: Dict[str, Any]
    workflow_id: Optional[str] = None


class InitWorkflowResponse(BaseModel):
    workflow_id: str
    message: str


@router.post("/init", response_model=InitWorkflowResponse)
async def init_workflow(request: InitWorkflowRequest):
    workflow_id = request.workflow_id or str(uuid4())

    if workflow_id in workflow_instances:
        print(f"Workflow id {workflow_id} already exists")
        raise HTTPException(status_code=400, detail=f"Workflow ID '{workflow_id}' already exists")

    system = WorkflowSystem(wf_id=workflow_id, config=request.config)
    workflow_instances[workflow_id] = system

    return InitWorkflowResponse(
        workflow_id=workflow_id,
        message=f"Workflow {workflow_id} initialized successfully."
    )


@router.get("/list")
async def list_workflows() -> Dict[str, str]:
    return {wid: f"{workflow_instances[wid].name}" for wid in workflow_instances}


@router.get("/{workflow_id}")
async def get_workflow_by_id(workflow_id: str) -> Dict[str, str]:
    if workflow_id not in workflow_instances:
        raise HTTPException(status_code=404, detail="Workflow ID not found")
    return {"workflow_id": workflow_id, "status": "exists"}


# Helper function to access from chat_routes
def get_workflow(workflow_id: str) -> Optional[WorkflowSystem]:
    if workflow_id not in workflow_instances:
        return None
    return workflow_instances[workflow_id]
