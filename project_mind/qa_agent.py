"""Quality Assurance Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext

class QAAgent(BaseAgent):
    """Agent specialized in quality assurance"""
    
    def __init__(self):
        super().__init__(AgentType.QA)
    
    def get_system_prompt(self) -> str:
        return """You are a Quality Assurance AI assistant specializing in:
- Test scenario generation and coverage analysis
- Defect tracking and pattern analysis
- Quality metrics and reporting
- Test status and readiness assessment
- Risk-based testing recommendations
- Regression and edge case identification

Your responses should:
- Focus on quality and testing aspects
- Provide specific test scenarios when needed
- Analyze defect patterns and trends
- Assess test coverage and gaps
- Recommend testing priorities
- Highlight quality risks

When discussing quality:
- Report on defect counts and severity
- Mention test coverage status
- Identify untested areas
- Suggest test scenarios
- Flag quality risks
- Reference acceptance criteria

Format your response to help QA Engineers and QA Leads with testing strategy and execution."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch QA data"""
        data = {}
        
        # Get bugs from JIRA
        issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project, "type": "Bug"}
        )
        data["bugs"] = issues_response.get("issues", [])
        
        # Get all issues for test coverage analysis
        all_issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project}
        )
        data["all_issues"] = all_issues_response.get("issues", [])
        
        # Get requirements for test scenario generation
        pages_response = self.call_api(
            "/confluence/pages",
            params={"project": context.project}
        )
        data["requirements"] = pages_response.get("pages", [])
        
        # Get QA-related meetings
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project}
        )
        data["meetings"] = meetings_response.get("meetings", [])
        
        return data