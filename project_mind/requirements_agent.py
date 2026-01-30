"""Requirements Intelligence Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext

class RequirementsAgent(BaseAgent):
    """Agent specialized in requirements analysis"""
    
    def __init__(self):
        super().__init__(AgentType.REQUIREMENTS)
    
    def get_system_prompt(self) -> str:
        return """You are a Requirements Intelligence AI assistant specializing in:
- Requirements extraction and analysis
- User story mapping and traceability
- Acceptance criteria validation
- Requirements gap identification
- Stakeholder requirement synthesis
- Requirements-to-implementation mapping

Your responses should:
- Clearly explain requirements in plain language
- Identify gaps, ambiguities, or conflicts
- Link requirements to user stories and tasks
- Highlight acceptance criteria
- Reference source documents (Confluence, emails)

When discussing requirements:
- State the requirement clearly
- Explain the business value
- List acceptance criteria
- Mention related user stories/tasks
- Flag any missing information or questions

Format your response to help Business Analysts, Product Owners, and Developers understand requirements clearly."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch requirements data"""
        data = {}
        
        # Get Confluence pages (requirements docs)
        pages_response = self.call_api(
            "/confluence/pages",
            params={"project": context.project}
        )
        data["pages"] = pages_response.get("pages", [])
        
        # Get JIRA stories and epics
        issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project}
        )
        # Filter for stories and epics
        issues = issues_response.get("issues", [])
        data["stories"] = [
            i for i in issues 
            if i.get("type") in ["Story", "Epic"]
        ]
        
        # Get relevant emails about requirements
        emails_response = self.call_api(
            "/outlook/emails",
            params={"project": context.project}
        )
        emails = emails_response.get("emails", [])
        data["requirement_emails"] = [
            e for e in emails
            if any(tag in e.get("tags", []) for tag in ["requirements", "feedback", "stakeholder"])
        ]
        
        # Get meeting notes about requirements
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project}
        )
        data["meetings"] = meetings_response.get("meetings", [])
        
        return data