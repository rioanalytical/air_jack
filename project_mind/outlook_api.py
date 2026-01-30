"""Mock Outlook API"""
from fastapi import FastAPI, HTTPException
from typing import Optional
from datetime import datetime
from .mock_data.outlook_data import EMAILS

router = FastAPI()

@router.get("/outlook/emails")
def get_emails(
    project: Optional[str] = None,
    subject: Optional[str] = None,
    sender: Optional[str] = None,
    date_from: Optional[str] = None,
    tag: Optional[str] = None
):
    """Get emails with optional filters"""
    emails = EMAILS.copy()
    
    if project:
        emails = [e for e in emails if e.get("project") == project]
    if subject:
        subject_lower = subject.lower()
        emails = [e for e in emails if subject_lower in e.get("subject", "").lower()]
    if sender:
        emails = [e for e in emails if sender in e.get("from", "")]
    if date_from:
        emails = [e for e in emails if e.get("date") >= date_from]
    if tag:
        emails = [e for e in emails if tag in e.get("tags", [])]
    
    return {"emails": emails, "total": len(emails)}

@router.get("/outlook/emails/{email_id}")
def get_email(email_id: str):
    """Get specific email"""
    email = next((e for e in EMAILS if e.get("id") == email_id), None)
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email

@router.get("/outlook/threads/{thread_id}")
def get_thread(thread_id: str):
    """Get email thread"""
    thread_emails = [e for e in EMAILS if e.get("thread_id") == thread_id]
    if not thread_emails:
        raise HTTPException(status_code=404, detail="Thread not found")
    return {"thread_id": thread_id, "emails": thread_emails, "count": len(thread_emails)}

@router.get("/outlook/search")
def search_emails(query: str, project: Optional[str] = None):
    """Search emails"""
    query_lower = query.lower()
    results = []
    
    for email in EMAILS:
        if project and email.get("project") != project:
            continue
            
        if (query_lower in email.get("subject", "").lower() or 
            query_lower in email.get("body", "").lower()):
            results.append(email)
    
    return {"results": results, "total": len(results)}