"""Mock Zoom API"""
from fastapi import FastAPI, HTTPException
from typing import Optional
from .mock_data.zoom_data import MEETINGS

router = FastAPI()

@router.get("/zoom/meetings")
def get_meetings(
    project: Optional[str] = None,
    date_from: Optional[str] = None,
    search: Optional[str] = None
):
    """Get meeting recordings and transcripts"""
    meetings = MEETINGS.copy()
    
    if project:
        meetings = [m for m in meetings if m.get("project") == project]
    if date_from:
        meetings = [m for m in meetings if m.get("date") >= date_from]
    if search:
        search_lower = search.lower()
        meetings = [
            m for m in meetings 
            if search_lower in m.get("title", "").lower() 
            or search_lower in m.get("transcript", "").lower()
        ]
    
    return {"meetings": meetings, "total": len(meetings)}

@router.get("/zoom/meetings/{meeting_id}")
def get_meeting(meeting_id: str):
    """Get specific meeting"""
    meeting = next((m for m in MEETINGS if m.get("id") == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meeting

@router.get("/zoom/meetings/{meeting_id}/transcript")
def get_transcript(meeting_id: str):
    """Get meeting transcript"""
    meeting = next((m for m in MEETINGS if m.get("id") == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "meeting_id": meeting_id,
        "title": meeting.get("title"),
        "date": meeting.get("date"),
        "transcript": meeting.get("transcript"),
        "key_decisions": meeting.get("key_decisions", []),
        "action_items": meeting.get("action_items", [])
    }

@router.get("/zoom/search")
def search_meetings(query: str, project: Optional[str] = None):
    """Search meeting transcripts"""
    query_lower = query.lower()
    results = []
    
    for meeting in MEETINGS:
        if project and meeting.get("project") != project:
            continue
            
        if (query_lower in meeting.get("title", "").lower() or 
            query_lower in meeting.get("transcript", "").lower()):
            
            # Extract relevant snippets from transcript
            transcript = meeting.get("transcript", "")
            lines = transcript.split("\n")
            relevant_lines = [line for line in lines if query_lower in line.lower()]
            
            results.append({
                **meeting,
                "relevant_snippets": relevant_lines[:5]  # Top 5 matches
            })
    
    return {"results": results, "total": len(results)}