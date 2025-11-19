import os

class Config:
    # Configurazione Modello
    OLLAMA_MODEL = "llama3"
    OLLAMA_BASE_URL = "http://localhost:11434"
    
    # Vector Store
    CHROMA_PATH = "./chroma_db"
    COLLECTION_NAME = "steam_games"
    
    # Embeddings
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"

    # Default
    DEFAULT_TEMPERATURE = 0.0
    TOP_K_RETRIEVAL = 12
