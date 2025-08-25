import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer
from config import config

class PaperStorage:
    
    def __init__(self):
        if not config.is_configured():
            raise ValueError("Qdrant not configured. Set QDRANT_URL and QDRANT_API_KEY")
        
        self.client = QdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key
        )
        
        self.embeddings = SentenceTransformer('all-MiniLM-L6-v2')
        
        self.collection_name = "paperscope_papers"
        
        self._create_collection()
    
    def _create_collection(self):
        try:
            collections = self.client.get_collections()
            existing = [c.name for c in collections.collections]
            
            if self.collection_name not in existing:
                test_embedding = self.embeddings.encode("test")
                vector_size = len(test_embedding)
                
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=vector_size,
                        distance=qmodels.Distance.COSINE
                    )
                )
                print(f"Created collection: {self.collection_name}")
            else:
                print(f"Using existing collection: {self.collection_name}")
                
        except Exception as e:
            print(f"Failed to create collection: {e}")
            raise
    
    def store_papers(self, papers: List[Dict[str, Any]]) -> int:
        if not papers:
            return 0
        
        points = []
        for i, paper in enumerate(papers):
            text = f"{paper['title']} {paper['summary']}"
            
            embedding = self.embeddings.encode(text)
            
            point = qmodels.PointStruct(
                id=i,
                vector=embedding.tolist(),
                payload={
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "summary": paper["summary"],
                    "arxiv_id": paper["arxiv_id"],
                    "published": paper["published"],
                    "pdf_url": paper["pdf_url"],
                    "primary_category": paper["primary_category"]
                }
            )
            points.append(point)
        
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            print(f"Stored {len(papers)} papers")
            return len(papers)
        except Exception as e:
            print(f"Failed to store papers: {e}")
            raise
    
    def search_papers(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embeddings.encode(query)
        
        try:
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding.tolist(),
                limit=limit
            )
            
            papers = []
            for result in results:
                papers.append({
                    "title": result.payload["title"],
                    "authors": result.payload["authors"],
                    "summary": result.payload["summary"],
                    "arxiv_id": result.payload["arxiv_id"],
                    "published": result.payload["published"],
                    "pdf_url": result.payload["pdf_url"],
                    "primary_category": result.payload["primary_category"],
                    "similarity_score": result.score
                })
            
            return papers
            
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": info.name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count
            }
        except Exception as e:
            return
            
