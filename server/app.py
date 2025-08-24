from fastapi import FastAPI
import arxiv
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from storage import PaperStorage
from qa_system import QASystem

app = FastAPI(title="PaperScope Agentic")

# Initialize storage (will fail if not configured)
storage = None
try:
    storage = PaperStorage()
except Exception as e:
    print(f"Storage not initialized: {e}")

try:
    qa_system = QASystem()
except Exception as e:
    print("QA system is not initialized.")

@app.get("/")
async def root():
    return {"message": "PaperScope Agentic API"}

@app.get("/health")
async def health():
    storage_status = "not_configured"
    if storage:
        try:
            info = storage.get_collection_info()
            storage_status = "connected" if "error" not in info else "error"
        except:
            storage_status = "error"
    
    return {
        "status": "ok", 
        "message": "Server is running",
        "configured": config.is_configured(),
        "storage": storage_status
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

@app.post("/store/{topic}")
async def store_papers(topic: str, max_results: int = 5):
    if not storage:
        return {"error": "Storage not configured"}
    
    try:
        # First search for papers
        search_result = await search_papers(topic, max_results)
        if "error" in search_result:
            return search_result
        
        papers = search_result["papers"]
        
        # Store papers in Qdrant
        stored_count = storage.store_papers(papers)
        
        return {
            "topic": topic,
            "papers_searched": len(papers),
            "papers_stored": stored_count,
            "message": f"Successfully stored {stored_count} papers"
        }
        
    except Exception as e:
        return {"error": f"Storage failed: {str(e)}"}

@app.get("/storage/search")
async def search_stored_papers(query: str, limit: int = 5):
    """Search papers stored in Qdrant"""
    if not storage:
        return {"error": "Storage not configured"}
    
    try:
        papers = storage.search_papers(query, limit)
        return {
            "query": query,
            "papers_found": len(papers),
            "papers": papers
        }
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

@app.get("/storage/info")
async def get_storage_info():
    """Get information about the storage collection"""
    if not storage:
        return {"error": "Storage not configured"}
    
    try:
        info = storage.get_collection_info()
        return info
    except Exception as e:
        return {"error": f"Failed to get info: {str(e)}"}

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

app.post("/qa")
async def ask_question(request: dict):
    if not qa_system:
        return {"error": "QA system is not configured. Check GROQ API Key"}

    try: 
        question = request.get("question", "").strip()
        if not question:
            return {"error": "Question is needed."}

            result = qa_system.answer_question(question, max_content=3)

            return {
                "question": question,
                "answer": result['answer'],
                "sources_used": result['context_user'],
                "sources": result['sources'],
                "error": result['error']
            }
        
    except Exception as e:
        return {"error": "failed : str(e)"}

