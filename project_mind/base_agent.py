"""Base agent class"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import requests
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from config.settings import settings
from models.schema import AgentResponse, AgentType, QueryContext

class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )
        self.api_base_url = settings.MOCK_API_BASE_URL
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent"""
        pass
    
    @abstractmethod
    def fetch_relevant_data(self, context: QueryContext) -> Dict[str, Any]:
        """Fetch relevant data from APIs"""
        pass
    
    def call_api(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call mock API endpoint"""
        try:
            url = f"{self.api_base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "data": None}
    
    def process_query(self, context: QueryContext, additional_context: Dict[str, Any] = None) -> AgentResponse:
        """Process query and generate response"""
        
        # Fetch relevant data
        data = self.fetch_relevant_data(context)
        
        # Build prompt
        system_prompt = self.get_system_prompt()
        
        user_message = f"""
Persona: {context.persona}
Project: {context.project}
Query: {context.query}

Relevant Data:
{self._format_data(data)}

{f"Additional Context: {additional_context}" if additional_context else ""}

Please provide a comprehensive response based on the available data.
Include sources and reasoning for your response.
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_message)
        ])
        
        # Generate response
        chain = prompt | self.llm
        response = chain.invoke({})
        
        # Extract sources from data
        sources = self._extract_sources(data)
        
        return AgentResponse(
            agent_type=self.agent_type,
            content=response.content,
            confidence=0.9,
            sources=sources,
            metadata={"data_summary": self._summarize_data(data)}
        )
    
    def _format_data(self, data: Dict[str, Any]) -> str:
        """Format data for LLM consumption"""
        import json
        return json.dumps(data, indent=2, default=str)[:5000]  # Limit size
    
    def _extract_sources(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract sources from data"""
        sources = []
        
        # Extract from different data types
        if "issues" in data:
            for issue in data.get("issues", [])[:3]:
                sources.append({
                    "type": "jira",
                    "id": issue.get("key"),
                    "title": issue.get("summary")
                })
        
        if "pages" in data:
            for page in data.get("pages", [])[:3]:
                sources.append({
                    "type": "confluence",
                    "id": page.get("id"),
                    "title": page.get("title")
                })
        
        if "emails" in data:
            for email in data.get("emails", [])[:3]:
                sources.append({
                    "type": "outlook",
                    "id": email.get("id"),
                    "title": email.get("subject")
                })
        
        if "meetings" in data:
            for meeting in data.get("meetings", [])[:3]:
                sources.append({
                    "type": "zoom",
                    "id": meeting.get("id"),
                    "title": meeting.get("title")
                })
        
        return sources
    
    def _summarize_data(self, data: Dict[str, Any]) -> str:
        """Create summary of data fetched"""
        summary_parts = []
        
        if "issues" in data:
            summary_parts.append(f"{len(data.get('issues', []))} JIRA issues")
        if "pages" in data:
            summary_parts.append(f"{len(data.get('pages', []))} Confluence pages")
        if "emails" in data:
            summary_parts.append(f"{len(data.get('emails', []))} emails")
        if "meetings" in data:
            summary_parts.append(f"{len(data.get('meetings', []))} meeting transcripts")
        
        return ", ".join(summary_parts) if summary_parts else "No data fetched"