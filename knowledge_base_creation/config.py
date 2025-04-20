import torch

class Config:
    """Centralized configuration settings"""
    MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    VECTOR_STORE_PATH = "vector_store"