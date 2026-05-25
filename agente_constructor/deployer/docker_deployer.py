"""
Docker Deployment Manager for Generated Agents
"""
import docker
from docker.errors import DockerException, ImageNotFound, APIError
from typing import Dict, Any, Optional
from pathlib import Path
import tempfile
import shutil
from config import settings


class DockerDeployer:
    """Manages Docker-based agent deployment"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
        except DockerException as e:
            raise RuntimeError(f"Failed to connect to Docker: {e}")
    
    def build_agent_image(
        self,
        agent_id: str,
        files: Dict[str, str],
        tag: Optional[str] = None
    ) -> str:
        """
        Build Docker image for agent
        
        Args:
            agent_id: Unique agent identifier
            files: Dict of {filename: content}
            tag: Optional custom tag
        
        Returns:
            Image ID
        """
        if tag is None:
            tag = f"{settings.agent_container_prefix}{agent_id}:latest"
        
        # Create temporary build context
        with tempfile.TemporaryDirectory() as tmpdir:
            build_path = Path(tmpdir)
            
            # Write all files
            for filename, content in files.items():
                file_path = build_path / filename
                file_path.write_text(content, encoding="utf-8")
            
            try:
                # Build image
                image, build_logs = self.client.images.build(
                    path=str(build_path),
                    tag=tag,
                    rm=True,
                    pull=False,
                    labels={
                        "agent.id": agent_id,
                        "generator": "agente_constructor",
                        "platform": "genes"
                    }
                )
                
                return image.id
            
            except docker.errors.BuildError as e:
                raise RuntimeError(f"Failed to build image: {e}")
    
    def deploy_agent(
        self,
        agent_id: str,
        image_id: str,
        port: Optional[int] = None,
        environment: Optional[Dict[str, str]] = None,
        network: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Deploy agent container
        
        Args:
            agent_id: Unique agent identifier
            image_id: Docker image ID or tag
            port: Host port to expose (auto-assigned if None)
            environment: Environment variables
            network: Docker network name
        
        Returns:
            Dict with container_id, port, status
        """
        container_name = f"{settings.agent_container_prefix}{agent_id}"
        
        # Prepare configuration
        container_config = {
            "image": image_id,
            "name": container_name,
            "detach": True,
            "labels": {
                "agent.id": agent_id,
                "platform": "genes",
                "managed_by": "agente_constructor"
            },
            "environment": environment or {},
            "restart_policy": {"Name": "unless-stopped"},
        }
        
        # Port mapping
        if port:
            container_config["ports"] = {"8000/tcp": port}
        else:
            container_config["ports"] = {"8000/tcp": None}  # Auto-assign
        
        # Network
        if network:
            container_config["network"] = network
        
        try:
            # Deploy container
            container = self.client.containers.run(**container_config)
            
            # Get assigned port
            container.reload()
            port_bindings = container.attrs["NetworkSettings"]["Ports"]
            assigned_port = None
            if "8000/tcp" in port_bindings and port_bindings["8000/tcp"]:
                assigned_port = int(port_bindings["8000/tcp"][0]["HostPort"])
            
            return {
                "container_id": container.id,
                "container_name": container_name,
                "port": assigned_port,
                "status": container.status,
                "image": image_id
            }
        
        except APIError as e:
            raise RuntimeError(f"Failed to deploy container: {e}")
    
    def stop_agent(self, container_id: str, remove: bool = False) -> bool:
        """Stop (and optionally remove) agent container"""
        try:
            container = self.client.containers.get(container_id)
            container.stop(timeout=10)
            
            if remove:
                container.remove()
            
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to stop container: {e}")
    
    def get_agent_status(self, container_id: str) -> Dict[str, Any]:
        """Get agent container status"""
        try:
            container = self.client.containers.get(container_id)
            container.reload()
            
            return {
                "id": container.id,
                "name": container.name,
                "status": container.status,
                "created": container.attrs["Created"],
                "ports": container.attrs["NetworkSettings"]["Ports"],
                "health": container.attrs.get("State", {}).get("Health", {}),
            }
        except Exception as e:
            raise RuntimeError(f"Failed to get status: {e}")
    
    def list_agents(self) -> list:
        """List all deployed agent containers"""
        filters = {
            "label": "platform=genes"
        }
        
        containers = self.client.containers.list(all=True, filters=filters)
        
        return [
            {
                "id": c.id,
                "name": c.name,
                "status": c.status,
                "agent_id": c.labels.get("agent.id"),
                "image": c.image.tags[0] if c.image.tags else c.image.id
            }
            for c in containers
        ]
