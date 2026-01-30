"""Mock JIRA API"""
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from .mock_data.jira_data import JIRA_ISSUES, SPRINTS, VELOCITY_HISTORY

router = FastAPI()

@router.get("/jira/issues")
def get_issues(
    project: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    assignee: Optional[str] = None,
    component: Optional[str] = None
):
    """Get JIRA issues with optional filters"""
    issues = JIRA_ISSUES.copy()
    
    if project:
        issues = [i for i in issues if i.get("project") == project]
    if status:
        issues = [i for i in issues if i.get("status") == status]
    if priority:
        issues = [i for i in issues if i.get("priority") == priority]
    if assignee:
        issues = [i for i in issues if i.get("assignee") == assignee]
    if component:
        issues = [i for i in issues if component in i.get("components", [])]
    
    return {"issues": issues, "total": len(issues)}

@router.get("/jira/issues/{issue_key}")
def get_issue(issue_key: str):
    """Get specific JIRA issue"""
    issue = next((i for i in JIRA_ISSUES if i.get("key") == issue_key), None)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.get("/jira/sprints")
def get_sprints(project: Optional[str] = None, status: Optional[str] = None):
    """Get sprint information"""
    sprints = SPRINTS.copy()
    
    if project:
        sprints = [s for s in sprints if s.get("project") == project]
    if status:
        sprints = [s for s in sprints if s.get("status") == status]
    
    return {"sprints": sprints}

@router.get("/jira/sprints/{sprint_id}")
def get_sprint(sprint_id: str):
    """Get specific sprint"""
    sprint = next((s for s in SPRINTS if s.get("id") == sprint_id), None)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.get("/jira/velocity")
def get_velocity(project: Optional[str] = None):
    """Get velocity history"""
    velocity = VELOCITY_HISTORY.copy()
    
    if project:
        velocity = [v for v in velocity if v.get("project") == project]
    
    return {"velocity_history": velocity}

@router.get("/jira/blockers")
def get_blockers(project: Optional[str] = None):
    """Get all blocked issues"""
    blockers = [i for i in JIRA_ISSUES if i.get("status") == "Blocked"]
    
    if project:
        blockers = [b for b in blockers if b.get("project") == project]
    
    return {"blockers": blockers, "total": len(blockers)}