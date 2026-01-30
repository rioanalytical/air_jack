"""Project Management Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext

class ProjectManagementAgent(BaseAgent):
    """Agent specialized in project management tasks"""
    
    def __init__(self):
        super().__init__(AgentType.PM)
    
    def get_system_prompt(self) -> str:
        return """You are a Project Management AI assistant specializing in:
- Sprint progress tracking and burndown analysis
- Velocity trends and team capacity
- Blocker identification and escalation
- Risk assessment and mitigation
- Status reporting and stakeholder communication
- Resource allocation and team workload

Your responses should be:
- Data-driven with specific metrics
- Action-oriented with clear next steps
- Risk-aware highlighting potential issues
- Concise yet comprehensive

When discussing blockers, always include:
- Issue ID and summary
- How long it's been blocked
- Owner/assignee
- Impact on sprint/project
- Suggested escalation if needed

Format your response professionally for project managers and leadership."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch project management data"""
        data = {}
        
        # Get JIRA data
        # Blocked issues
        blockers_response = self.call_api(
            "/jira/blockers",
            params={"project": context.project}
        )
        data["blockers"] = blockers_response.get("blockers", [])
        
        # Sprint information
        sprints_response = self.call_api(
            "/jira/sprints",
            params={"project": context.project, "status": "Active"}
        )
        data["sprints"] = sprints_response.get("sprints", [])
        
        # Velocity history
        velocity_response = self.call_api(
            "/jira/velocity",
            params={"project": context.project}
        )
        data["velocity_history"] = velocity_response.get("velocity_history", [])
        
        # All issues for the project
        issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project}
        )
        data["issues"] = issues_response.get("issues", [])
        
        # Get email updates about the project
        emails_response = self.call_api(
            "/outlook/emails",
            params={"project": context.project}
        )
        data["emails"] = emails_response.get("emails", [])[:5]  # Limit to recent 5
        
        # Get recent meeting notes
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project}
        )
        data["meetings"] = meetings_response.get("meetings", [])[:3]  # Recent 3
        
        return data