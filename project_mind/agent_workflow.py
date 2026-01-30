"""LangGraph workflow for multi-agent orchestration"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from models.state import AgentState
from models.schema import QueryContext, AgentType, IntentCategory
from agents.orchestrator_agent import OrchestratorAgent
from agents.pm_agent import ProjectManagementAgent
from agents.requirements_agent import RequirementsAgent
from agents.dev_context_agent import DevContextAgent
from agents.qa_agent import QAAgent
from agents.communication_agent import CommunicationAgent
from agents.report_generation_agent import ReportGenerationAgent
from config.settings import settings

class AgentWorkflow:
    """Multi-agent workflow using LangGraph"""
    
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        
        # Initialize all agents
        self.agents = {
            AgentType.PM: ProjectManagementAgent(),
            AgentType.REQUIREMENTS: RequirementsAgent(),
            AgentType.DEV_CONTEXT: DevContextAgent(),
            AgentType.QA: QAAgent(),
            AgentType.COMMUNICATION: CommunicationAgent(),
            AgentType.REPORT_GENERATION: ReportGenerationAgent()
        }
        
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.TEMPERATURE,
            api_key=settings.OPENAI_API_KEY
        )
        
        # Build workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Create state graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("orchestrate", self._orchestrate_node)
        workflow.add_node("execute_agents", self._execute_agents_node)
        workflow.add_node("synthesize", self._synthesize_node)
        
        # Define edges
        workflow.set_entry_point("orchestrate")
        workflow.add_edge("orchestrate", "execute_agents")
        workflow.add_edge("execute_agents", "synthesize")
        workflow.add_edge("synthesize", END)
        
        return workflow.compile()
    
    def _orchestrate_node(self, state: AgentState) -> AgentState:
        """Orchestrator node - decides which agents to invoke"""
        try:
            context = state["query_context"]
            decision = self.orchestrator.decide_routing(context)
            
            state["orchestrator_decision"] = decision
            state["reasoning_chain"].append(
                f"Orchestrator Decision: Intent={decision.intent.value}, "
                f"Agents={[a.value for a in decision.selected_agents]}, "
                f"Reasoning={decision.reasoning}"
            )
            
        except Exception as e:
            state["errors"].append(f"Orchestration error: {str(e)}")
        
        return state
    
    def _execute_agents_node(self, state: AgentState) -> AgentState:
        """Execute selected agents in parallel"""
        try:
            decision = state["orchestrator_decision"]
            context = state["query_context"]
            
            agent_responses = []
            
            # Execute each selected agent
            for agent_type in decision.selected_agents:
                try:
                    agent = self.agents.get(agent_type)
                    if agent:
                        response = agent.process_query(context)
                        agent_responses.append(response)
                        state["reasoning_chain"].append(
                            f"Agent {agent_type.value} executed: {response.metadata.get('data_summary', 'N/A')}"
                        )
                        
                        # Collect sources
                        state["sources"].extend(response.sources)
                        
                except Exception as e:
                    state["errors"].append(f"Agent {agent_type.value} error: {str(e)}")
            
            state["agent_responses"] = agent_responses
            
        except Exception as e:
            state["errors"].append(f"Agent execution error: {str(e)}")
        
        return state
    
    def _synthesize_node(self, state: AgentState) -> AgentState:
        """Synthesize responses from all agents into final response"""
        try:
            context = state["query_context"]
            decision = state["orchestrator_decision"]
            agent_responses = state["agent_responses"]
            
            # If report generation was requested, use report agent
            if decision.intent == IntentCategory.GENERATE_REPORT:
                report_agent = self.agents.get(AgentType.REPORT_GENERATION)
                if report_agent:
                    report_response = report_agent.generate_status_report(context, agent_responses)
                    state["final_response"] = report_response.content
                    return state
            
            # Otherwise synthesize responses
            if not agent_responses:
                state["final_response"] = "I couldn't find relevant information to answer your query."
                return state
            
            # Aggregate all agent responses
            aggregated_content = "\n\n---\n\n".join([
                f"**From {resp.agent_type.value.replace('_', ' ').title()} Agent:**\n{resp.content}"
                for resp in agent_responses
            ])
            
            # Use LLM to synthesize
            synthesis_prompt = ChatPromptTemplate.from_messages([
                ("system", """You are a synthesis AI that combines multiple agent responses into a cohesive answer.
Your job is to:
1. Integrate information from multiple sources
2. Remove redundancy
3. Organize information logically
4. Maintain all important details
5. Provide a clear, comprehensive response

Create a well-structured response that flows naturally."""),
                ("user", f"""
Persona: {context.persona}
Query: {context.query}

Agent Responses:
{aggregated_content}

Synthesize these responses into a single, coherent answer that directly addresses the user's query.
""")
            ])
            
            chain = synthesis_prompt | self.llm
            response = chain.invoke({})
            
            state["final_response"] = response.content
            state["reasoning_chain"].append("Synthesized final response from all agent outputs")
            
        except Exception as e:
            state["errors"].append(f"Synthesis error: {str(e)}")
            # Fallback: just concatenate responses
            state["final_response"] = "\n\n".join([
                resp.content for resp in state["agent_responses"]
            ])
        
        return state
    
    def process_query(self, query_context: QueryContext) -> Dict[str, Any]:
        """Process a user query through the workflow"""
        
        # Initialize state
        initial_state: AgentState = {
            "query_context": query_context,
            "orchestrator_decision": None,
            "agent_responses": [],
            "final_response": None,
            "sources": [],
            "reasoning_chain": [],
            "errors": []
        }
        
        # Run workflow
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "response": final_state["final_response"],
            "sources": final_state["sources"],
            "reasoning": final_state["reasoning_chain"],
            "errors": final_state["errors"],
            "intent": final_state["orchestrator_decision"].intent.value if final_state["orchestrator_decision"] else None,
            "agents_used": [a.value for a in final_state["orchestrator_decision"].selected_agents] if final_state["orchestrator_decision"] else []
        }