"""
API Request/Response Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class AgentCreateRequest(BaseModel):
    """Request to create a new agent"""
    name: str = Field(..., min_length=3, max_length=128)
    description: Optional[str] = None
    purpose: str = Field(..., min_length=10, description="Natural language description of what the agent should do")
    capabilities: Optional[List[str]] = Field(default_factory=list)
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    auto_approve: bool = Field(default=False, description="Skip manual approval (admin only)")


class AgentResponse(BaseModel):
    """Agent information response"""
    id: int
    agent_id: str
    name: str
    description: Optional[str]
    status: str
    purpose: str
    capabilities: List[str]
    container_id: Optional[str]
    exposed_port: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentApproveRequest(BaseModel):
    """Request to approve a pending agent"""
    agent_id: str
    approved_by: str = Field(..., min_length=1)
    notes: Optional[str] = None


class TaskCreateRequest(BaseModel):
    """Request to create a task"""
    task_type: str = Field(..., min_length=1)
    payload: Dict[str, Any]
    agent_id: Optional[str] = None
    priority: int = Field(default=0, ge=0, le=10)


class TaskResponse(BaseModel):
    """Task information response"""
    id: int
    task_id: str
    agent_id: Optional[str]
    task_type: str
    status: str
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    
    class Config:
        from_attributes = True


class AgentLogResponse(BaseModel):
    """Agent log entry"""
    id: int
    agent_id: str
    event_type: str
    message: Optional[str]
    timestamp: datetime
    level: str
    
    class Config:
        from_attributes = True


class StatusResponse(BaseModel):
    """Platform status"""
    total_agents: int
    active_agents: int
    pending_approval: int
    tasks_queued: int
    tasks_running: int
    system_healthy: bool
