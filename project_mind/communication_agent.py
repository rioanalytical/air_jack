"""Communication & Collaboration Agent"""
from typing import Dict, Any
from .base_agent import BaseAgent
from models.schema import AgentType, QueryContext

class CommunicationAgent(BaseAgent):
    """Agent specialized in communication analysis"""
    
    def __init__(self):
        super().__init__(AgentType.COMMUNICATION)
    
    def get_system_prompt(self) -> str:
        return """You are a Communication Intelligence AI assistant specializing in:
- Email thread analysis and summarization
- Meeting transcript extraction and key points
- Decision tracking and attribution
- Action item identification
- Stakeholder communication analysis
- Discussion context and history

Your responses should:
- Summarize communications clearly
- Extract key decisions and who made them
- Identify action items with owners
- Provide context from discussions
- Track conversation threads
- Highlight important updates

When discussing communications:
- Summarize the main points
- Extract key decisions
- List action items with owners and deadlines
- Mention relevant participants
- Provide email/meeting references
- Highlight urgent or important items

Format your response to help all personas understand what was communicated and decided."""
    
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch communication data"""
        data = {}
        
        # Get project emails
        emails_response = self.call_api(
            "/outlook/emails",
            params={"project": context.project}
        )
        data["emails"] = emails_response.get("emails", [])
        
        # Get meeting transcripts
        meetings_response = self.call_api(
            "/zoom/meetings",
            params={"project": context.project}
        )
        data["meetings"] = meetings_response.get("meetings", [])
        
        # Extract action items and decisions from meetings
        action_items = []
        key_decisions = []
        
        for meeting in data["meetings"]:
            action_items.extend(meeting.get("action_items", []))
            key_decisions.extend(meeting.get("key_decisions", []))
        
        data["all_action_items"] = action_items
        data["all_key_decisions"] = key_decisions
        
        return data