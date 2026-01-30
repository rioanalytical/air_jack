"""Streamlit UI for ProjectMind AI"""
import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import settings
from models.schema import QueryContext, Persona
from workflows.agent_workflow import AgentWorkflow

# Page config
st.set_page_config(
    page_title="ProjectMind AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .response-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .source-box {
        background-color: #fff;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
    }
    .reasoning-box {
        background-color: #fffef0;
        padding: 1rem;
        border-radius: 5px;
        border-left: 3px solid #ffa500;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "workflow" not in st.session_state:
    st.session_state.workflow = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

# Header
st.markdown('<div class="main-header">🤖 ProjectMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Agentic AI System for Software Development Projects</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=settings.OPENAI_API_KEY,
        help="Enter your OpenAI API key"
    )
    
    if api_key and api_key != settings.OPENAI_API_KEY:
        settings.OPENAI_API_KEY = api_key
        st.session_state.api_key_set = True
        st.success("✅ API Key set!")
    elif api_key:
        st.session_state.api_key_set = True
    
    st.divider()
    
    # Persona selection
    st.subheader("👤 Select Your Persona")
    persona = st.selectbox(
        "Who are you?",
        options=settings.PERSONAS,
        index=0,
        help="Select your role in the project"
    )
    
    # Project selection
    st.subheader("📁 Select Project")
    project = st.selectbox(
        "Which project?",
        options=settings.PROJECTS,
        index=0,
        help="Select the project you want to query"
    )
    
    # Intent category (optional)
    st.subheader("🎯 Intent Category (Optional)")
    intent = st.selectbox(
        "What do you want to do?",
        options=["Auto-detect"] + settings.INTENT_CATEGORIES,
        index=0,
        help="The system will auto-detect if not specified"
    )
    
    st.divider()
    
    # System info
    st.subheader("ℹ️ System Info")
    st.info(f"""
    **Mock API Server:**  
    {settings.MOCK_API_BASE_URL}
    
    **LLM Model:**  
    {settings.LLM_MODEL}
    
    **Available Agents:**
    - Orchestrator
    - Project Management
    - Requirements
    - Dev Context
    - QA
    - Communication
    - Report Generation
    """)
    
    if st.button("Clear Conversation"):
        st.session_state.conversation_history = []
        st.rerun()

# Main content
if not st.session_state.api_key_set or not settings.OPENAI_API_KEY:
    st.warning("⚠️ Please enter your OpenAI API key in the sidebar to continue.")
    st.info("""
    **How to get an OpenAI API key:**
    1. Go to https://platform.openai.com/
    2. Sign up or log in
    3. Navigate to API keys
    4. Create a new secret key
    """)
    st.stop()

# Initialize workflow
if st.session_state.workflow is None:
    with st.spinner("Initializing AI agents..."):
        try:
            st.session_state.workflow = AgentWorkflow()
            st.success("✅ AI agents initialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to initialize agents: {str(e)}")
            st.stop()

# Example queries
st.subheader("💡 Example Queries")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Sprint Status"):
        example_query = "What's the status of the current sprint? Show me progress and any blockers."
        st.session_state.example_query = example_query

with col2:
    if st.button("🚫 Show Blockers"):
        example_query = "What are all the active blockers for this project?"
        st.session_state.example_query = example_query

with col3:
    if st.button("📈 Generate Report"):
        example_query = "Generate a status report for leadership covering progress, risks, and next steps."
        st.session_state.example_query = example_query

# Query input
st.subheader("💬 Ask a Question")
query_text = st.text_area(
    "Enter your query:",
    value=st.session_state.get("example_query", ""),
    height=100,
    placeholder="e.g., What are the acceptance criteria for the OAuth2 authentication feature?"
)

if "example_query" in st.session_state:
    del st.session_state.example_query

# Process query
if st.button("🚀 Submit Query", type="primary", use_container_width=True):
    if not query_text:
        st.warning("Please enter a query.")
    else:
        # Create query context
        context = QueryContext(
            persona=Persona(persona),
            project=project,
            query=query_text
        )
        
        # Show processing
        with st.spinner("🤖 AI agents are processing your query..."):
            try:
                # Process query
                result = st.session_state.workflow.process_query(context)
                
                # Store in history
                st.session_state.conversation_history.append({
                    "persona": persona,
                    "project": project,
                    "query": query_text,
                    "result": result
                })
                
                # Display results
                st.success("✅ Query processed successfully!")
                
                # Main response
                st.markdown("### 📝 Response")
                st.markdown(f'<div class="response-box">{result["response"]}</div>', unsafe_allow_html=True)
                
                # Metadata in expandable sections
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.expander("🎯 Intent & Agents Used", expanded=False):
                        st.write(f"**Detected Intent:** {result['intent']}")
                        st.write(f"**Agents Invoked:** {', '.join(result['agents_used'])}")
                
                with col2:
                    with st.expander("📚 Sources", expanded=False):
                        if result["sources"]:
                            for i, source in enumerate(result["sources"], 1):
                                st.markdown(f"""
                                <div class="source-box">
                                <strong>{i}. {source.get('type', 'Unknown').upper()}</strong><br>
                                {source.get('title', 'N/A')}<br>
                                <small>ID: {source.get('id', 'N/A')}</small>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No sources available")
                
                with st.expander("🔍 Reasoning Chain", expanded=False):
                    for i, reason in enumerate(result["reasoning"], 1):
                        st.markdown(f'<div class="reasoning-box"><strong>Step {i}:</strong> {reason}</div>', unsafe_allow_html=True)
                
                if result["errors"]:
                    with st.expander("⚠️ Errors", expanded=False):
                        for error in result["errors"]:
                            st.error(error)
                
            except Exception as e:
                st.error(f"❌ Error processing query: {str(e)}")
                st.exception(e)

# Conversation history
if st.session_state.conversation_history:
    st.divider()
    st.subheader("📜 Conversation History")
    
    for i, conv in enumerate(reversed(st.session_state.conversation_history), 1):
        with st.expander(f"Query {len(st.session_state.conversation_history) - i + 1}: {conv['query'][:100]}...", expanded=False):
            st.write(f"**Persona:** {conv['persona']}")
            st.write(f"**Project:** {conv['project']}")
            st.write(f"**Query:** {conv['query']}")
            st.markdown("**Response:**")
            st.markdown(conv['result']['response'])

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>ProjectMind AI - Intelligent Project Management Assistant</p>
    <p style='font-size: 0.8rem;'>Powered by LangGraph, LangChain, and OpenAI</p>
</div>
""", unsafe_allow_html=True)