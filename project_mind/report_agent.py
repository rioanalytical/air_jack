"""Report Generation Agent"""
from typing import Dict, Any, List
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext, AgentResponse

class ReportGenerationAgent(BaseAgent):
    """Agent specialized in generating formatted reports"""
    
    def __init__(self):
        super().__init__(AgentType.REPORT_GENERATION)
    
    def get_system_prompt(self) -> str:
        return """You are a Report Generation AI assistant specializing in:
- Creating structured status reports
- Generating executive summaries
- Formatting sprint reviews and retrospectives
- Creating stakeholder updates
- Building risk registers
- Producing progress dashboards

Your responses should be:
- Well-formatted with clear sections
- Professional and executive-ready
- Data-driven with specific metrics
- Concise yet comprehensive
- Visually organized with headers and bullets

Report Structure Guidelines:
- Start with an executive summary
- Use clear section headers
- Include metrics and data points
- Highlight risks and blockers
- End with recommendations or next steps

Format reports professionally for leadership and stakeholders."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch comprehensive data for report generation"""
        data = {}
        
        # Get all JIRA data
        issues_response = self.call_api(
            "/jira/issues",
            params={"project": context.project}
        )
        data["issues"] = issues_response.get("issues", [])
        
        # Get sprint data
        sprints_response = self.call_api(
            "/jira/sprints",
            params={"project": context.project, "status": "Active"}
        )
        data["sprints"] = sprints_response.get("sprints", [])
        
        # Get velocity
        velocity_response = self.call_api(
            "/jira/velocity",
            params={"project": context.project}
        )
        data["velocity"] = velocity_response.get("velocity_history", [])
        
        # Get blockers
        blockers_response = self.call_api(
            "/jira/blockers",
            params={"project": context.project}
        )
        data["blockers"] = blockers_response.get("blockers", [])
        
        # Get recent meetings
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project}
        )
        data["meetings"] = meetings_response.get("meetings", [])
        
        return data
    
    def generate_status_report(self, context: QueryContext, agent_responses: List[AgentResponse]) -> AgentResponse:
        """Generate a comprehensive status report"""
        
        # Aggregate data from other agents
        all_data = self.fetch_relevant_data(context)
        
        # Synthesize information from other agents
        agent_insights = "\n\n".join([
            f"**{resp.agent_type.value.upper()}:**\n{resp.content[:500]}"
            for resp in agent_responses
        ])
        
        system_prompt = self.get_system_prompt()
        
        user_message = f"""
Generate a comprehensive status report for:
Project: {context.project}
Requested by: {context.persona}

Data Available:
{self._format_data(all_data)}

Insights from Specialized Agents:
{agent_insights}

Create a well-structured status report that includes:
1. Executive Summary
2. Sprint Progress
3. Key Accomplishments
4. Active Blockers and Risks
5. Upcoming Milestones
6. Recommendations
"""
        
        from langchain.prompts import ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_message)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=response.content,
            confidence=0.95,
            sources=self._extract_sources(all_data),
            metadata={"report_type": "status_report"}
        )