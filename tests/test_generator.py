"""
Tests for Agent Generator
"""
import pytest
from agente_constructor.generator import AgentGenerator


def test_generate_agent_id():
    """Test agent ID generation"""
    generator = AgentGenerator(templates_dir="agente_constructor/templates")
    
    agent_id = generator.generate_agent_id("Test Agent")
    
    assert agent_id.startswith("test_agent_")
    assert len(agent_id) > len("test_agent_")


def test_analyze_purpose_database():
    """Test purpose analysis detects database need"""
    generator = AgentGenerator(templates_dir="agente_constructor/templates")
    
    purpose = "Create an agent that stores data in a database"
    analysis = generator.analyze_purpose(purpose)
    
    assert analysis["needs_database"] is True


def test_analyze_purpose_api():
    """Test purpose analysis detects API need"""
    generator = AgentGenerator(templates_dir="agente_constructor/templates")
    
    purpose = "Create an agent that exposes REST API endpoints"
    analysis = generator.analyze_purpose(purpose)
    
    assert analysis["is_api"] is True


def test_generate_requirements():
    """Test requirements.txt generation"""
    generator = AgentGenerator(templates_dir="agente_constructor/templates")
    
    spec = {
        "analysis": {
            "needs_database": True,
            "needs_redis": True,
            "needs_http_client": False
        }
    }
    
    requirements = generator.generate_requirements(spec)
    
    assert "fastapi" in requirements
    assert "asyncpg" in requirements
    assert "redis" in requirements


@pytest.mark.skip(reason="Requires template files")
def test_generate_agent_complete():
    """Test complete agent generation"""
    generator = AgentGenerator(templates_dir="agente_constructor/templates")
    
    result = generator.generate_agent(
        name="Test Agent",
        purpose="A test agent for unit testing",
        description="Testing agent generation"
    )
    
    assert "agent_id" in result
    assert "files" in result
    assert "main.py" in result["files"]
    assert "Dockerfile" in result["files"]
    assert "requirements.txt" in result["files"]
