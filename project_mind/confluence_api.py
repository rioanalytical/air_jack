"""Mock Confluence API"""
from fastapi import FastAPI, HTTPException
from typing import Optional
from .mock_data.confluence_data import CONFLUENCE_PAGES

router = FastAPI()

@router.get("/confluence/pages")
def get_pages(
    project: Optional[str] = None,
    space: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None
):
    """Get Confluence pages with optional filters"""
    pages = CONFLUENCE_PAGES.copy()
    
    if project:
        pages = [p for p in pages if p.get("project") == project]
    if space:
        pages = [p for p in pages if p.get("space") == space]
    if tag:
        pages = [p for p in pages if tag in p.get("tags", [])]
    if search:
        search_lower = search.lower()
        pages = [
            p for p in pages 
            if search_lower in p.get("title", "").lower() 
            or search_lower in p.get("content", "").lower()
        ]
    
    return {"pages": pages, "total": len(pages)}

@router.get("/confluence/pages/{page_id}")
def get_page(page_id: str):
    """Get specific Confluence page"""
    page = next((p for p in CONFLUENCE_PAGES if p.get("id") == page_id), None)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.get("/confluence/search")
def search_content(query: str, project: Optional[str] = None):
    """Search Confluence content"""
    query_lower = query.lower()
    results = []
    
    for page in CONFLUENCE_PAGES:
        if project and page.get("project") != project:
            continue
            
        if (query_lower in page.get("title", "").lower() or 
            query_lower in page.get("content", "").lower()):
            # Calculate relevance score (simple)
            score = 0
            if query_lower in page.get("title", "").lower():
                score += 10
            score += page.get("content", "").lower().count(query_lower)
            
            results.append({
                **page,
                "relevance_score": score
            })
    
    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return {"results": results, "total": len(results)}