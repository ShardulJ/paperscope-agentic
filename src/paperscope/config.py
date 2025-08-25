import os
from typing import Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class Config(BaseModel):
    groq_api_key: Optional[str] = None
    qdrant_url: Optional[str] = None
    qdrant_api_key: Optional[str] = None
    
    def load_from_env(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.qdrant_url = os.getenv("QDRANT_URL")
        self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
    
    def is_configured(self) -> bool:
        return bool(self.groq_api_key and self.qdrant_url and self.qdrant_api_key)

config = Config()
config.load_from_env()
