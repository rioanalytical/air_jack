"""Data models and schemas"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class Persona(str, Enum):
    DEVELOPER = "Developer"
    QA_ENGINEER = "QA Engineer"
    PROJECT_MANAGER = "Project Manager"
    PRODUCT_OWNER = "Product Owner"
    SCRUM_MASTER = "Scrum Master"
    BUSINESS_ANALYST = "Business Analyst"
    BUSINESS_DATA_ANALYST = "Business Data Analyst"

class IntentCategory(str, Enum):
    GET_INFORMATION = "Get Information"
    GENERATE_REPORT = "Generate Report"
    TRACK_PROGRESS = "Track Progress"
    IDENTIFY_RISKS = "Identify Risks"
    GET_RECOMMENDATIONS = "Get Recommendations"
    UNDERSTAND_REQUIREMENTS = "Understand Requirements"
    REVIEW_QUALITY = "Review Quality"
    CHECK_STATUS = "Check Status"

class AgentType(str, Enum):
    ORCHESTRATOR = "orchestrator"
    REQUIREMENTS = "requirements"
    DEV_CONTEXT = "dev_context"
    QA = "qa"
    PM = "pm"
    PRODUCT = "product"
    COMMUNICATION = "communication"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    SEMANTIC_SEARCH = "semantic_search"
    REPORT_GENERATION = "report_generation"

class QueryContext(BaseModel):
    """Context for user query"""
    persona: Persona
    project: str
    intent: Optional[IntentCategory] = None
    query: str
    
class AgentResponse(BaseModel):
    """Response from an agent"""
    agent_type: AgentType
    content: str
    confidence: float = 1.0
    sources: List[Dict[str, Any]] = []
    metadata: Dict[str, Any] = {}

class OrchestratorDecision(BaseModel):
    """Decision made by orchestrator"""
    intent: IntentCategory
    selected_agents: List[AgentType]
    reasoning: str
    context: Dict[str, Any] = {}