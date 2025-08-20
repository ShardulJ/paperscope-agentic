from fastapi import FastAPI
import arxiv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

app = FastAPI(title="PaperScope Agentic")

@app.get("/")
async def root():
    return {"message": "PaperScope Agentic API"}

@app.get("/health")
async def health():
    """Check server health and configuration status"""
    return {
        "status": "ok", 
        "message": "Server is running",
        "configured": config.is_configured(),
        "missing_keys": []
    }

@app.get("/search/{topic}")
async def search_papers(topic: str, max_results: int = 5):
    try:
        client = arxiv.Client(
            page_size=100,
            delay_seconds=3,
            num_retries=3
        )
        
        search = arxiv.Search(
            query=topic,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        papers = []
        for result in client.results(search):
            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "arxiv_id": result.entry_id.split('/')[-1],
                "published": result.published.isoformat() if result.published else None,
                "pdf_url": result.pdf_url,
                "primary_category": result.primary_category
            }
            papers.append(paper)
        
        return {
            "topic": topic,
            "papers_found": len(papers),
            "papers": papers
        }
        
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

@app.get("/config/status")
async def config_status():
    """Check configuration status"""
    missing = []
    if not config.groq_api_key:
        missing.append("GROQ_API_KEY")
    if not config.qdrant_url:
        missing.append("QDRANT_URL")
    if not config.qdrant_api_key:
        missing.append("QDRANT_API_KEY")
    
    return {
        "configured": config.is_configured(),
        "missing_keys": missing,
        "has_groq": bool(config.groq_api_key),
        "has_qdrant": bool(config.qdrant_url and config.qdrant_api_key)
    }
