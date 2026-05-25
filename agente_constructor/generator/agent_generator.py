"""
Agent Code Generation Engine
"""
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import uuid
import yaml


class AgentGenerator:
    """Generates agent code from templates and specifications"""
    
    def __init__(self, templates_dir: str):
        self.templates_dir = Path(templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def generate_agent_id(self, name: str) -> str:
        """Generate unique agent ID"""
        safe_name = name.lower().replace(" ", "_").replace("-", "_")
        unique_suffix = uuid.uuid4().hex[:8]
        return f"{safe_name}_{unique_suffix}"
    
    def analyze_purpose(self, purpose: str) -> Dict[str, Any]:
        """
        Analyze agent purpose and extract requirements
        
        In production, this would use LLM to parse intent.
        For now, basic keyword matching.
        """
        purpose_lower = purpose.lower()
        
        analysis = {
            "needs_database": any(kw in purpose_lower for kw in ["database", "store", "save", "persist"]),
            "needs_redis": any(kw in purpose_lower for kw in ["cache", "queue", "task"]),
            "needs_http_client": any(kw in purpose_lower for kw in ["api", "fetch", "request", "http"]),
            "needs_scheduler": any(kw in purpose_lower for kw in ["schedule", "cron", "periodic"]),
            "is_worker": any(kw in purpose_lower for kw in ["worker", "process", "task", "job"]),
            "is_api": any(kw in purpose_lower for kw in ["api", "endpoint", "rest", "serve"]),
        }
        
        return analysis
    
    def generate_dockerfile(self, agent_spec: Dict[str, Any]) -> str:
        """Generate Dockerfile for agent"""
        template = self.env.get_template("agent.Dockerfile.j2")
        return template.render(**agent_spec)
    
    def generate_main_py(self, agent_spec: Dict[str, Any]) -> str:
        """Generate main.py for agent"""
        template = self.env.get_template("agent_main.py.j2")
        return template.render(**agent_spec)
    
    def generate_requirements(self, agent_spec: Dict[str, Any]) -> str:
        """Generate requirements.txt for agent"""
        base_requirements = [
            "fastapi==0.115.0",
            "uvicorn[standard]==0.32.0",
            "pydantic==2.9.0",
            "python-dotenv==1.0.1",
        ]
        
        analysis = agent_spec.get("analysis", {})
        
        if analysis.get("needs_database"):
            base_requirements.extend([
                "asyncpg==0.30.0",
                "sqlalchemy==2.0.36",
            ])
        
        if analysis.get("needs_redis"):
            base_requirements.extend([
                "redis==5.2.0",
                "hiredis==3.0.0",
            ])
        
        if analysis.get("needs_http_client"):
            base_requirements.append("httpx==0.28.1")
        
        if analysis.get("needs_scheduler"):
            base_requirements.append("apscheduler==3.10.4")
        
        return "\n".join(sorted(set(base_requirements)))
    
    def generate_agent(
        self,
        name: str,
        purpose: str,
        description: str = "",
        capabilities: List[str] = None,
        config: Dict[str, Any] = None
    ) -> Dict[str, str]:
        """
        Generate complete agent codebase
        
        Returns dict with file contents:
        {
            "agent_id": "...",
            "files": {
                "main.py": "...",
                "Dockerfile": "...",
                "requirements.txt": "...",
                "config.yaml": "..."
            }
        }
        """
        agent_id = self.generate_agent_id(name)
        analysis = self.analyze_purpose(purpose)
        
        agent_spec = {
            "agent_id": agent_id,
            "name": name,
            "description": description or f"Auto-generated agent: {name}",
            "purpose": purpose,
            "capabilities": capabilities or [],
            "config": config or {},
            "analysis": analysis,
        }
        
        files = {
            "main.py": self.generate_main_py(agent_spec),
            "Dockerfile": self.generate_dockerfile(agent_spec),
            "requirements.txt": self.generate_requirements(agent_spec),
            "config.yaml": yaml.dump(agent_spec["config"], default_flow_style=False),
        }
        
        return {
            "agent_id": agent_id,
            "files": files,
            "spec": agent_spec
        }
