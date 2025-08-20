# PaperScope Agentic

A research paper assistant that helps you find and analyze academic papers.

## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see Configuration section)
4. Run the server: `uvicorn server.app:app --reload`

## Configuration

Create a `.env` file in the root directory with your API keys:

```bash
# Groq API (get free tokens at https://console.groq.com/)
GROQ_API_KEY=your_groq_api_key_here

# Qdrant Cloud (free tier at https://cloud.qdrant.io/)
QDRANT_URL=https://your-cluster.qdrant.tech:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

## Features

- Search arXiv for research papers
- Get paper metadata (title, authors, summary, PDF links)
- Configuration management for API keys
- RESTful API endpoints

## API Endpoints

- `GET /` - API information
- `GET /health` - Server health check and configuration status
- `GET /config/status` - Detailed configuration status
- `GET /search/{topic}` - Search arXiv for papers on a topic
  - Optional query param: `max_results` (default: 5)

## Example Usage

```bash
# Check server health and config
curl "http://localhost:8000/health"

# Check configuration status
curl "http://localhost:8000/config/status"

# Search for papers on machine learning
curl "http://localhost:8000/search/machine%20learning?max_results=3"
```

## Next Steps

- [x] Basic server setup
- [x] arXiv search functionality
- [x] Configuration management
- [ ] Document storage with Qdrant
- [ ] Q&A with Groq LLM
- [ ] Advanced features

*Building this step by step...*
