import os
from typing import List, Dict, Any
from langchain_groq import ChatGroq
from storage import PaperStorage
from config import config

class QASystem:
    def __init__(self):
        if not config.is_configured():
            raise ValueError("Config is not configured")
        
        self.storage = PaperStorage()
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=config.groq_api_key,
        )

        self.prompt_template = """
        You are a helpful assistant that can answer questions about the following context:
        {context}

        Question: {question}
        Answer:
        """

    def answer_question(self, question: str, max_context: int = 3) -> Dict[str, Any]:
        try:
            context_papers = self.storage.search_papers(question, max_context)

            if not context_papers:
                return {
                    "answer": "No relevant papers found",
                    "source": [],
                    "context_used": 0,
                    "error": None
                }

            formatted_context = self._format_context(context_papers)

            prompt = self.prompt_template.format(context=formatted_context, question=question)

            response = self.llm.invoke(prompt)
            answer = response.content if hasattr(response, "content") else response

            return {
                "answer": answer,
                "source": context_papers,
                "context_used": len(context_papers),
                "error": None
            }

        except Exception as e:
            return {
                "answer": "An error occurred while answering the question",
                "source": [],
                "context_used": 0,
                "error": str(e)
            }

    def _format_context(self, papers: List[Dict]) -> str:
        if not papers:
            return "No papers"

        context = []
        for i, paper in enumerate(papers, start=1):
            context_part  = f"""
            Paper {i}:
            Title: {paper.get("title", "N/A")},
            Authors: {paper.get("authors", "N/A")},
            arxiv_id: {paper.get("arxiv_id", "N/A")},
            Category: {paper.get("primary_category", "N/A")},
            Summary: {paper.get("summary", "N/A")},
            """
            
            context.append(context_part)

        return "\n\n".join(context)

    def get_context_for_question(self, question: str, limit: int = 3) -> List[Dict]:
        try:
            return self.storage.search_papers(question, limit)
        except Exception as e:
            print(f"Error getting context for question: {e}")
            return []

    def test_connection(self) -> bool:
        try:
            test_response = self.llm.invoke("Say 'Hello' if you can hear me.")
            return "Hello" in str(test_response)
        except Exception as e:
            print(f"Connection failed: {e}")
            return

