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
- Store papers in Qdrant vector database
- Semantic search through stored papers
- Get paper metadata (title, authors, summary, PDF links)
- Configuration management for API keys
- RESTful API endpoints

## API Endpoints

- `GET /` - API information
- `GET /health` - Server health check and configuration status
- `GET /config/status` - Detailed configuration status
- `GET /search/{topic}` - Search arXiv for papers on a topic
  - Optional query param: `max_results` (default: 5)
- `POST /store/{topic}` - Search arXiv and store papers in Qdrant
  - Optional query param: `max_results` (default: 5)
- `GET /storage/search` - Search stored papers by semantic similarity
  - Query params: `query` (required), `limit` (default: 5)
- `GET /storage/info` - Get information about stored papers

## Example Usage

```bash
# Check server health and config
curl "http://localhost:8000/health"

# Check configuration status
curl "http://localhost:8000/config/status"

# Search for papers on machine learning
curl "http://localhost:8000/search/machine%20learning?max_results=3"

# Store papers on transformer architecture
curl -X POST "http://localhost:8000/store/transformer%20architecture?max_results=5"

# Search stored papers
curl "http://localhost:8000/storage/search?query=attention%20mechanisms&limit=3"

# Get storage info
curl "http://localhost:8000/storage/info"
```

## How It Works

1. **Search**: Use `/search/{topic}` to find papers on arXiv
2. **Store**: Use `/store/{topic}` to save papers to Qdrant with embeddings
3. **Retrieve**: Use `/storage/search` to find similar papers semantically

## Next Steps

- [x] Basic server setup
- [x] arXiv search functionality
- [x] Configuration management
- [x] Document storage with Qdrant
- [ ] Q&A with Groq LLM
- [ ] Advanced features

*Building this step by step...*
