from torch import Tensor
from sentence_transformers import SentenceTransformer

class EmbeddingModel():
    def __init__(self):
        self.embedding_model = SentenceTransformer("keepitreal/vietnamese-sbert")
        
    def get_embedding(self, text: str) -> list:
        if not text.strip():
            return []

        embedding = self.encode(text)
        return embedding.tolist()
    
    def encode(self, text: str) -> Tensor:
        return self.embedding_model.encode(text)
