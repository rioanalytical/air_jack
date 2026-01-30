# ProjectMind AI - Agentic AI System for Software Development

An intelligent multi-agent AI system that helps different personas in software development projects by aggregating information from multiple sources and providing contextual insights.

## 🌟 Features

- **Multi-Agent Architecture**: Specialized agents for different domains (PM, QA, Dev, Requirements, etc.)
- **LangGraph Orchestration**: Intelligent routing and coordination between agents
- **Multi-Source Integration**: Connects to JIRA, Confluence, Outlook, Zoom, and more
- **Persona-Based Responses**: Tailored responses for different roles
- **Real-time Analysis**: Processes queries through specialized agents in parallel
- **Report Generation**: Creates formatted reports for stakeholders

## 🏗️ System Architecture

```
User Query → Orchestrator → Specialized Agents → Synthesizer → Response
                  ↓              ↓
            Intent Analysis   Parallel Execution
                  ↓              ↓
            Agent Selection   Data Fetching (JIRA, Confluence, etc.)
```

### Available Agents

1. **Orchestrator Agent**: Routes queries to appropriate agents
2. **Project Management Agent**: Sprint progress, velocity, blockers
3. **Requirements Agent**: Requirements analysis and traceability
4. **Dev Context Agent**: Technical documentation and architecture
5. **QA Agent**: Test scenarios, defects, quality metrics
6. **Communication Agent**: Email and meeting analysis
7. **Report Generation Agent**: Formatted reports and summaries

## 📋 Prerequisites

- Python 3.9+
- OpenAI API key
- Git

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd project_mind_ai
```

2. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## 🎮 Usage

### Step 1: Start Mock API Server

In one terminal, start the mock API server:

```bash
python -m mock_apis
```

This starts a FastAPI server at `http://localhost:8000` with mock data for:
- JIRA issues, sprints, velocity
- Confluence pages
- Outlook emails
- Zoom meeting transcripts

### Step 2: Launch Streamlit App

In another terminal, launch the Streamlit UI:

```bash
streamlit run app/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 3: Use the System

1. **Select Your Persona**: Choose your role (Developer, QA, PM, etc.)
2. **Select Project**: Choose the project to query
3. **Enter Query**: Ask questions about your project
4. **View Results**: Get AI-powered insights with sources and reasoning

## 💡 Example Queries

### For Project Managers:
- "What are the active blockers for the Payment Gateway project?"
- "Generate a status report for Sprint 15"
- "Show me the velocity trend for the last 6 sprints"

### For Developers:
- "What's the approved approach for implementing OAuth2?"
- "Explain the caching strategy for microservices"
- "Show me all tasks assigned to the Backend Team"

### For QA Engineers:
- "What are the critical defects blocking release?"
- "Generate test scenarios for the payment gateway feature"
- "What's the defect density by module?"

### For Business Analysts:
- "What are the acceptance criteria for the OAuth2 feature?"
- "Which requirements are not yet mapped to stories?"
- "Show me all pending requirement clarifications"

### For Product Owners:
- "What's the business justification for the mobile app rewrite?"
- "Summarize stakeholder feedback from the Q1 roadmap"
- "Which roadmap items are at risk?"

## 🗂️ Project Structure

```
project_mind_ai/
├── agents/                 # Specialized AI agents
│   ├── base_agent.py      # Base agent class
│   ├── orchestrator_agent.py
│   ├── pm_agent.py
│   ├── requirements_agent.py
│   ├── dev_context_agent.py
│   ├── qa_agent.py
│   ├── communication_agent.py
│   └── report_generation_agent.py
├── mock_apis/             # Mock API endpoints
│   ├── jira_api.py
│   ├── confluence_api.py
│   ├── outlook_api.py
│   ├── zoom_api.py
│   └── mock_data/         # Synthetic data
├── models/                # Data models
│   ├── schema.py          # Pydantic models
│   └── state.py           # LangGraph state
├── workflows/             # LangGraph workflows
│   └── agent_workflow.py  # Multi-agent orchestration
├── app/                   # Streamlit UI
│   └── streamlit_app.py
├── config/                # Configuration
│   └── settings.py
└── requirements.txt
```

## 🔧 Configuration

### Settings (config/settings.py)

- `LLM_MODEL`: OpenAI model to use (default: gpt-4-turbo-preview)
- `TEMPERATURE`: LLM temperature (default: 0.7)
- `MOCK_API_PORT`: Port for mock API server (default: 8000)

### Supported Personas

- Developer
- QA Engineer
- Project Manager
- Product Owner
- Scrum Master
- Business Analyst
- Business Data Analyst

### Available Projects (Mock Data)

- Payment Gateway Integration
- Mobile App Rewrite
- Customer Dashboard v2.0
- API Migration Project

## 🧪 Mock Data

The system includes comprehensive mock data:

### JIRA Data
- 7 issues across different projects
- Sprint information with velocity tracking
- Blocked issues with details
- Historical velocity data

### Confluence Pages
- Technical specifications
- Requirements documents
- Architecture decisions
- Product roadmaps

### Email Threads
- Project communications
- Stakeholder feedback
- Technical discussions
- Status updates

### Meeting Transcripts
- Sprint planning meetings
- Architecture reviews
- Daily standups
- Key decisions and action items

## 🔄 Workflow Process

1. **User submits query** with persona and project context
2. **Orchestrator analyzes** the query to determine intent
3. **Agent selection** based on intent and persona
4. **Parallel execution** of selected agents
5. **Data fetching** from relevant sources (JIRA, Confluence, etc.)
6. **LLM processing** to generate insights
7. **Response synthesis** combining all agent outputs
8. **Formatted response** with sources and reasoning

## 🎯 Key Features

### Intelligent Routing
The orchestrator automatically determines which agents to invoke based on:
- Query content and intent
- User persona
- Project context

### Multi-Source Integration
Agents fetch data from multiple systems:
- JIRA for tickets and sprints
- Confluence for documentation
- Outlook for emails
- Zoom for meeting transcripts

### Context-Aware Responses
Responses are tailored for each persona:
- Technical details for developers
- Quality metrics for QA
- Business value for product owners
- Status summaries for project managers

### Reasoning Transparency
Every response includes:
- Sources used
- Agents involved
- Step-by-step reasoning
- Confidence scores

## 🛠️ Extending the System

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement required methods:
   - `get_system_prompt()`
   - `fetch_relevant_data()`
3. Register in `AgentWorkflow`

### Adding New Data Sources

1. Create new API module in `mock_apis/`
2. Add mock data in `mock_apis/mock_data/`
3. Mount router in `mock_apis/__init__.py`
4. Update agents to fetch from new source

### Customizing Prompts

Edit system prompts in each agent's `get_system_prompt()` method to customize behavior.

## 📊 Performance Considerations

- **Parallel Agent Execution**: Agents run concurrently for faster responses
- **Data Caching**: API responses can be cached to reduce latency
- **Token Management**: Responses are limited to avoid token limits
- **Error Handling**: Graceful degradation if agents fail

## 🔒 Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement proper authentication for production use
- Sanitize user inputs
- Implement rate limiting

## 🚧 Future Enhancements

- [ ] Real API integrations (JIRA, Confluence, etc.)
- [ ] Vector database for semantic search
- [ ] Knowledge graph for relationship tracking
- [ ] User authentication and authorization
- [ ] Conversation memory and context
- [ ] Proactive alerts and notifications
- [ ] Custom agent creation interface
- [ ] Analytics dashboard
- [ ] Multi-project support
- [ ] API for third-party integrations

## 📝 License

MIT License - feel free to use and modify

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Support

For issues, questions, or suggestions, please open a GitHub issue.

## 🙏 Acknowledgments

- Built with LangChain and LangGraph
- Powered by OpenAI GPT models
- UI created with Streamlit
- Mock APIs using FastAPI

---

**Note**: This is a demonstration system with mock data. For production use, integrate with real APIs and implement proper authentication, authorization, and data security measures.