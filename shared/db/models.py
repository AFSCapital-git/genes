"""
Database Models for Genes Platform
"""
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AgentStatus(str, Enum):
    """Agent lifecycle status"""
    PENDING = "pending"
    APPROVED = "approved"
    DEPLOYING = "deploying"
    RUNNING = "running"
    PAUSED = "paused"
    FAILED = "failed"
    TERMINATED = "terminated"


class Agent(Base):
    """Agent Registry Model"""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(64), unique=True, nullable=False, index=True)
    name = Column(String(128), nullable=False)
    description = Column(Text)
    
    # Status
    status = Column(String(32), default=AgentStatus.PENDING)
    
    # Configuration
    purpose = Column(Text, nullable=False)
    capabilities = Column(JSON, default=list)
    config = Column(JSON, default=dict)
    
    # Deployment
    container_id = Column(String(128))
    image_name = Column(String(256))
    exposed_port = Column(Integer)
    
    # Security
    requires_approval = Column(Boolean, default=True)
    approved_by = Column(String(128))
    approved_at = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(128), default="agente_constructor")
    
    # Audit
    generation_prompt = Column(Text)
    generation_metadata = Column(JSON, default=dict)


class AgentLog(Base):
    """Agent Activity Log"""
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(64), index=True, nullable=False)
    
    # Event
    event_type = Column(String(32), nullable=False)
    event_data = Column(JSON)
    message = Column(Text)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    level = Column(String(16), default="INFO")


class Task(Base):
    """Task Queue for Agent Work"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(64), unique=True, nullable=False, index=True)
    
    # Assignment
    agent_id = Column(String(64), index=True)
    
    # Task Details
    task_type = Column(String(64), nullable=False)
    payload = Column(JSON, nullable=False)
    priority = Column(Integer, default=0)
    
    # Status
    status = Column(String(32), default="pending")
    result = Column(JSON)
    error = Column(Text)
    
    # Timing
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Metadata
    created_by = Column(String(128))
    retry_count = Column(Integer, default=0)
