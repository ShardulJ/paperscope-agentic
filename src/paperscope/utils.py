from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text:str, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter

def clean_summary(summary: str) -> str:
    return " ".join(summary.split())