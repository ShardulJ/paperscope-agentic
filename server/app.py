from fastapi import FastAPI
import arxiv

app = FastAPI(title="PaperScope Agentic")

@app.get("/")
async def root():
    return {"message": "PaperScope Agentic API"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Server is running"}

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
