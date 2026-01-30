"""Orchestrator Agent - Routes queries to appropriate agents"""
from typing import Dict, Any
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config.settings import settings
from models.schema import QueryContext, OrchestratorDecision, AgentType, IntentCategory
import json

class OrchestratorAgent:
    """Master orchestrator that routes queries to appropriate agents"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0.3,  # Lower temperature for more consistent routing
            api_key=settings.OPENAI_API_KEY
        )
    
    def decide_routing(self, context: QueryContext) -> OrchestratorDecision:
        """Decide which agents to invoke based on query"""
        
        system_prompt = """You are an intelligent query router for a project management AI system.
Your job is to analyze user queries and determine:
1. The intent category
2. Which specialized agents should handle the query
3. Reasoning for your decision

Available Agents:
- requirements: Requirements Intelligence Agent (requirements, user stories, acceptance criteria)
- dev_context: Development Context Agent (technical docs, architecture, code patterns)
- qa: Quality Assurance Agent (test scenarios, defects, quality metrics)
- pm: Project Management Agent (sprint progress, velocity, blockers, status)
- product: Product Strategy Agent (roadmap, business goals, stakeholder feedback)
- communication: Communication Agent (emails, meetings, decisions, action items)
- knowledge_graph: Knowledge Graph Agent (relationships, dependencies, traceability)
- semantic_search: Semantic Search Agent (advanced search across all sources)
- report_generation: Report Generation Agent (formatted reports, summaries)

Intent Categories:
- Get Information: Simple factual queries
- Generate Report: Create formatted reports or summaries
- Track Progress: Sprint/project progress queries
- Identify Risks: Find blockers, risks, issues
- Get Recommendations: Suggest actions or improvements
- Understand Requirements: Requirements and specifications
- Review Quality: Testing, defects, quality metrics
- Check Status: Current status of items

Respond ONLY with a JSON object in this exact format:
{
    "intent": "intent_category",
    "agents": ["agent1", "agent2"],
    "reasoning": "explanation of why these agents were selected"
}"""

        user_message = f"""
Persona: {context.persona}
Project: {context.project}
Query: {context.query}

Determine the intent and select appropriate agents to handle this query.
"""

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", user_message)
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        
        # Parse JSON response
        try:
            decision_data = json.loads(response.content)
            
            # Map string intent to enum
            intent_map = {
                "Get Information": IntentCategory.GET_INFORMATION,
                "Generate Report": IntentCategory.GENERATE_REPORT,
                "Track Progress": IntentCategory.TRACK_PROGRESS,
                "Identify Risks": IntentCategory.IDENTIFY_RISKS,
                "Get Recommendations": IntentCategory.GET_RECOMMENDATIONS,
                "Understand Requirements": IntentCategory.UNDERSTAND_REQUIREMENTS,
                "Review Quality": IntentCategory.REVIEW_QUALITY,
                "Check Status": IntentCategory.CHECK_STATUS
            }
            
            intent = intent_map.get(decision_data.get("intent"), IntentCategory.GET_INFORMATION)
            
            # Map agent strings to enums
            agent_map = {
                "requirements": AgentType.REQUIREMENTS,
                "dev_context": AgentType.DEV_CONTEXT,
                "qa": AgentType.QA,
                "pm": AgentType.PM,
                "product": AgentType.PRODUCT,
                "communication": AgentType.COMMUNICATION,
                "knowledge_graph": AgentType.KNOWLEDGE_GRAPH,
                "semantic_search": AgentType.SEMANTIC_SEARCH,
                "report_generation": AgentType.REPORT_GENERATION
            }
            
            agents = [
                agent_map.get(a, AgentType.SEMANTIC_SEARCH) 
                for a in decision_data.get("agents", [])
            ]
            
            return OrchestratorDecision(
                intent=intent,
                selected_agents=agents,
                reasoning=decision_data.get("reasoning", ""),
                context={}
            )
            
        except json.JSONDecodeError:
            # Fallback to semantic search if parsing fails
            return OrchestratorDecision(
                intent=IntentCategory.GET_INFORMATION,
                selected_agents=[AgentType.SEMANTIC_SEARCH],
                reasoning="Failed to parse routing decision, defaulting to semantic search",
                context={}
            )