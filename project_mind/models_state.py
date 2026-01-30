"""State management for LangGraph workflow"""
from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from .schema import QueryContext, AgentResponse, OrchestratorDecision

class AgentState(TypedDict):
    """State passed between agents in the workflow"""
    
    # Input
    query_context: QueryContext
    
    # Orchestrator output
    orchestrator_decision: Optional[OrchestratorDecision]
    
    # Agent responses
    agent_responses: List[AgentResponse]
    
    # Final synthesized response
    final_response: Optional[str]
    
    # Metadata
    sources: List[Dict[str, Any]]
    reasoning_chain: List[str]
    
    # Error handling
    errors: List[str]