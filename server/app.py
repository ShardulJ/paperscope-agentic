"""
FastAPI server for PaperScope Agentic RAG Server.
"""

from fastapi import FastAPI

app = FastAPI(title="PaperScope Agentic")

@app.get("/")
async def root():
    return {"message": "PaperScope Agentic API"}

@app.get("/health")
async def health():
    return {"status": "ok", "message": "Server is running"}
