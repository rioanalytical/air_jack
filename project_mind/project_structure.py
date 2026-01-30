"""
ProjectMind AI - Directory Structure

project_mind_ai/
│
├── README.md
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── mock_apis/
│   ├── __init__.py
│   ├── jira_api.py
│   ├── confluence_api.py
│   ├── outlook_api.py
│   ├── sharepoint_api.py
│   ├── zoom_api.py
│   └── mock_data/
│       ├── __init__.py
│       ├── jira_data.py
│       ├── confluence_data.py
│       ├── outlook_data.py
│       ├── sharepoint_data.py
│       └── zoom_data.py
│
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── orchestrator_agent.py
│   ├── requirements_agent.py
│   ├── dev_context_agent.py
│   ├── qa_agent.py
│   ├── pm_agent.py
│   ├── product_agent.py
│   ├── communication_agent.py
│   ├── knowledge_graph_agent.py
│   ├── semantic_search_agent.py
│   └── report_generation_agent.py
│
├── models/
│   ├── __init__.py
│   ├── schema.py
│   └── state.py
│
├── storage/
│   ├── __init__.py
│   ├── vector_store.py
│   └── knowledge_graph.py
│
├── utils/
│   ├── __init__.py
│   ├── llm_utils.py
│   └── helpers.py
│
├── workflows/
│   ├── __init__.py
│   └── agent_workflow.py
│
└── app/
    ├── __init__.py
    └── streamlit_app.py

"""
