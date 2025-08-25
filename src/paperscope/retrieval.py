import arxiv
from typing import List, Dict

def fetch_papers(query: str, max_results: int = 5) -> List[Dict]:
    client = arxiv.Client(page_size=100, delay_seconds=3, num_retries=3)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    for result in client.results(search):
        papers.append({
            "title": result.title,
            "authors": [a.name for a in result.authors],
            "summary": result.summary,
            "arxiv_id": result.entry_id.split("/")[-1],
            "published": result.published.isoformat() if result.published else None,
            "pdf_url": result.pdf_url,
            "primary_category": result.primary_category
        })
    
    return papers