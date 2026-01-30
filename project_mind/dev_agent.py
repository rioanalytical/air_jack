"""Development Context Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext

class DevContextAgent(BaseAgent):
    """Agent specialized in development context"""
    
    def __init__(self):
        super().__init__(AgentType.DEV_CONTEXT)
    
    def get_system_prompt(self) -> str:
        return """You are a Development Context AI assistant specializing in:
- Technical architecture and design decisions
- Code patterns and best practices
- Development standards and conventions
- Technical blockers and dependencies
- Implementation guidance
- Technical documentation

Your responses should:
- Provide clear technical guidance
- Reference architecture decisions and documentation
- Explain code patterns and approaches
- Highlight technical dependencies
- Suggest best practices
- Include code examples when relevant

When discussing technical topics:
- Explain the technical approach clearly
- Reference relevant documentation
- Mention related components/services
- Highlight dependencies and blockers
- Provide implementation guidance

Format your response to help Developers and Tech Leads with technical implementation."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch development context data"""
        data = {}
        
        # Get technical Confluence pages
        pages_response = self.call_api(
            "/confluence/pages",
            params={"project": context.project, "space": "Engineering"}
        )
        data["tech_docs"] = pages_response.get("pages", [])
        
        # Get development tasks from JIRA
        issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project}
        )
        issues = issues_response.get("issues", [])
        data["dev_tasks"] = [
            i for i in issues 
            if i.get("type") in ["Task", "Story", "Bug"]
        ]
        
        # Get architecture meeting notes
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project, "search": "architecture"}
        )
        data["arch_meetings"] = meetings_response.get("meetings", [])
        
        # Get technical emails
        emails_response = self.call_api(
            "/outlook/search",
            params={"query": "architecture technical", "project": context.project}
        )
        data["tech_emails"] = emails_response.get("results", [])[:5]
        
        return data