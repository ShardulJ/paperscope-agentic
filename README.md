# PaperScope Agentic

A research paper assistant that helps you find and analyze academic papers.

## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables
4. Run the server: `uvicorn server.app:app --reload`

## Features

- Search arXiv for research papers
- Get paper metadata (title, authors, summary, PDF links)
- RESTful API endpoints

## API Endpoints

- `GET /` - API information
- `GET /health` - Server health check
- `GET /search/{topic}` - Search arXiv for papers on a topic
  - Optional query param: `max_results` (default: 5)

## Example Usage

```bash
# Search for papers on machine learning
curl "http://localhost:8000/search/machine%20learning?max_results=3"

# Health check
curl "http://localhost:8000/health"
```

*More features coming soon...*
