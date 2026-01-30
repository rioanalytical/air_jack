"""Mock API Server - Aggregates all mock APIs"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from .jira_api import router as jira_router
from .confluence_api import router as confluence_router
from .outlook_api import router as outlook_router
from .zoom_api import router as zoom_router

app = FastAPI(title="ProjectMind Mock APIs", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.mount("/jira", jira_router)
app.mount("/confluence", confluence_router)
app.mount("/outlook", outlook_router)
app.mount("/zoom", zoom_router)

@app.get("/")
def root():
    return {
        "message": "ProjectMind AI Mock API Server",
        "version": "1.0.0",
        "endpoints": {
            "jira": "/jira/*",
            "confluence": "/confluence/*",
            "outlook": "/outlook/*",
            "zoom": "/zoom/*"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the mock API server"""
    print(f"Starting ProjectMind Mock API Server on {host}:{port}")
    print(f"Available endpoints:")
    print(f"  - JIRA: http://{host}:{port}/jira")
    print(f"  - Confluence: http://{host}:{port}/confluence")
    print(f"  - Outlook: http://{host}:{port}/outlook")
    print(f"  - Zoom: http://{host}:{port}/zoom")
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()