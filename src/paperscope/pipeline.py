import argparse
from .retrieval import fetch_papers
from .ingest import PaperStorage
from .rag import ask

def run_pipeline(topic: str, question: str):
    storage = PaperStorage()
    papers = fetch_papers(topic, max_results=5)
    storage.store_papers(papers)

    print(f"Stored {len(papers)} papers for topic: {topic}")
    response = ask(question)
    print("Answer:", response["answer"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--question", required=True)
    args = parser.parse_args()
    run_pipeline(args.topic, args.question)