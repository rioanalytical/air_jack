# ProjectMind AI - Complete Setup Guide

## 🎯 Quick Start (5 Minutes)

### Prerequisites
- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Terminal/Command Prompt

### Step-by-Step Setup

#### 1. Install Python Dependencies

```bash
# Create project directory
mkdir project_mind_ai
cd project_mind_ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install requirements
pip install streamlit==1.32.0 langchain==0.1.16 langchain-openai==0.1.1 langgraph==0.0.38 fastapi==0.110.0 uvicorn==0.27.1 pydantic==2.6.3 python-dotenv==1.0.1 chromadb==0.4.24 tiktoken==0.6.0 openai==1.14.0 networkx==3.2.1 pandas==2.2.1 numpy==1.26.4 requests==2.31.0
```

#### 2. Create Project Structure

Create all the files provided in the artifacts with the exact directory structure:

```
project_mind_ai/
├── config/
│   ├── __init__.py
│   └── settings.py
├── mock_apis/
│   ├── __init__.py
│   ├── jira_api.py
│   ├── confluence_api.py
│   ├── outlook_api.py
│   ├── zoom_api.py
│   └── mock_data/
│       ├── __init__.py
│       ├── jira_data.py
│       ├── confluence_data.py
│       ├── outlook_data.py
│       └── zoom_data.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── orchestrator_agent.py
│   ├── pm_agent.py
│   ├── requirements_agent.py
│   ├── dev_context_agent.py
│   ├── qa_agent.py
│   ├── communication_agent.py
│   └── report_generation_agent.py
├── models/
│   ├── __init__.py
│   ├── schema.py
│   └── state.py
├── workflows/
│   ├── __init__.py
│   └── agent_workflow.py
├── app/
│   ├── __init__.py
│   └── streamlit_app.py
├── .env
├── requirements.txt
├── run_mock_server.py
└── README.md
```

#### 3. Create Empty __init__.py Files

```bash
# Create empty __init__.py files in each directory
touch config/__init__.py
touch mock_apis/__init__.py
touch mock_apis/mock_data/__init__.py
touch agents/__init__.py
touch models/__init__.py
touch workflows/__init__.py
touch app/__init__.py
```

#### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# .env file content
OPENAI_API_KEY=your_openai_api_key_here
MOCK_API_HOST=localhost
MOCK_API_PORT=8000
LLM_MODEL=gpt-4-turbo-preview
EMBEDDING_MODEL=text-embedding-3-small
TEMPERATURE=0.7
```

**Replace `your_openai_api_key_here` with your actual OpenAI API key!**

#### 5. Start the Mock API Server

Open a terminal and run:

```bash
python run_mock_server.py
```

You should see:
```
Starting ProjectMind Mock API Server on 0.0.0.0:8000
Available endpoints:
  - JIRA: http://0.0.0.0:8000/jira
  - Confluence: http://0.0.0.0:8000/confluence
  - Outlook: http://0.0.0.0:8000/outlook
  - Zoom: http://0.0.0.0:8000/zoom
```

Keep this terminal running!

#### 6. Launch the Streamlit App

Open a **new terminal** (keep the first one running), activate your virtual environment, and run:

```bash
# Activate venv again
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Streamlit app
streamlit run app/streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎮 Using the System

### Basic Workflow

1. **Enter API Key** (if not in .env):
   - Enter your OpenAI API key in the sidebar
   - Click outside the text box to save

2. **Select Context**:
   - **Persona**: Choose your role (e.g., Developer, PM, QA)
   - **Project**: Select a project to query
   - **Intent**: Optional, auto-detected if not specified

3. **Ask Questions**:
   - Type your question in the text area
   - Click "Submit Query"
   - Wait for AI agents to process

4. **View Results**:
   - Main response with insights
   - Sources used
   - Reasoning chain
   - Agents involved

### Example Queries to Try

#### For Project Managers:
```
What are all the active blockers for the Payment Gateway Integration project?
```

```
Generate a comprehensive status report for Sprint 15 including progress, risks, and recommendations.
```

```
Show me the velocity trend and explain if there are any concerns.
```

#### For Developers:
```
What's the approved technical approach for implementing OAuth2 authentication?
```

```
Explain the caching strategy we should use in our microservices.
```

```
What are the open tasks for the payment module?
```

#### For QA Engineers:
```
What are the critical defects that need attention?
```

```
Generate test scenarios for the new payment gateway feature.
```

```
Which modules have the highest defect density?
```

#### For Business Analysts:
```
What are the acceptance criteria for the OAuth2 authentication feature?
```

```
Show me all requirements that are not yet mapped to user stories.
```

```
Are there any gaps or ambiguities in the payment gateway requirements?
```

#### For Product Owners:
```
What's the business justification for the mobile app rewrite?
```

```
Summarize the stakeholder feedback on our Q1 roadmap.
```

```
Which features are at risk for the Q1 release?
```

## 🔧 Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure you have all `__init__.py` files:
```bash
find . -name "__init__.py"
```

Should show:
```
./config/__init__.py
./mock_apis/__init__.py
./mock_apis/mock_data/__init__.py
./agents/__init__.py
./models/__init__.py
./workflows/__init__.py
./app/__init__.py
```

### Issue: "OpenAI API key not set"

**Solutions**:
1. Check your `.env` file has the correct key
2. Enter the key directly in the Streamlit sidebar
3. Verify the key is valid at https://platform.openai.com/

### Issue: "Connection refused to Mock API"

**Solutions**:
1. Make sure the mock API server is running (`python run_mock_server.py`)
2. Check the port is not in use by another application
3. Verify `MOCK_API_PORT` in `.env` matches the server port

### Issue: "Agents taking too long"

**Solutions**:
1. Check your internet connection
2. Verify OpenAI API is accessible
3. Try a simpler query first
4. Check OpenAI API usage limits

### Issue: Import errors with LangChain/LangGraph

**Solution**: Make sure all packages are installed:
```bash
pip install --upgrade langchain langchain-openai langgraph
```

## 📊 Understanding the Output

### Response Structure

**Main Response**: 
- Synthesized answer from multiple agents
- Formatted for your persona
- Includes specific data and recommendations

**Intent & Agents Used**:
- Detected intent category
- List of agents that processed the query
- Helps understand how the query was routed

**Sources**:
- JIRA issues referenced
- Confluence pages used
- Emails analyzed
- Meeting transcripts consulted

**Reasoning Chain**:
- Step-by-step process
- Shows how the system arrived at the answer
- Useful for debugging and transparency

## 🎓 Advanced Usage

### Customizing Agents

Edit the system prompt in any agent file to change behavior:

```python
# In agents/pm_agent.py
def get_system_prompt(self) -> str:
    return """Your custom prompt here..."""
```

### Adding New Mock Data

Edit the mock data files to add your own scenarios:

```python
# In mock_apis/mock_data/jira_data.py
JIRA_ISSUES = [
    {
        "id": "JIRA-NEW",
        "key": "PROJ-123",
        # ... your data
    }
]
```

### Adjusting LLM Parameters

In `.env` file:
```
LLM_MODEL=gpt-4-turbo-preview  # or gpt-3.5-turbo for faster/cheaper
TEMPERATURE=0.7  # Lower for more deterministic, higher for creative
```

## 🚀 Performance Tips

1. **Start with simple queries** to test the system
2. **Use auto-detect intent** instead of specifying manually
3. **Be specific** in your queries for better results
4. **Reference project names** explicitly when querying
5. **Use persona context** - different personas get different insights

## 📈 Next Steps

1. **Explore Different Personas**: Try each role to see specialized responses
2. **Test Complex Queries**: Combine multiple intents in one query
3. **Generate Reports**: Use the "Generate Report" intent for formatted outputs
4. **Analyze Patterns**: Look at the reasoning chain to understand agent behavior
5. **Customize**: Modify prompts and add your own data

## 🐛 Known Limitations

- Mock data only - not connected to real systems
- Limited to provided projects and data
- No conversation memory between queries
- No authentication/authorization
- Single-user system (no multi-tenancy)

## 📞 Getting Help

1. Check the README.md for detailed documentation
2. Review error messages in the Streamlit interface
3. Check both terminal windows for error logs
4. Verify all files are created correctly
5. Ensure all dependencies are installed

## 🎉 Success Checklist

- [ ] Python 3.9+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Project structure created correctly
- [ ] All __init__.py files in place
- [ ] .env file created with API key
- [ ] Mock API server running (Terminal 1)
- [ ] Streamlit app running (Terminal 2)
- [ ] Successfully submitted a query
- [ ] Received a response from agents

Once all items are checked, you're ready to explore ProjectMind AI! 🚀

---

**Happy Querying! 🤖**