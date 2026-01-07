from config import TRANSFORMER_MODEL
from sentence_transformers import SentenceTransformer


class SemanticSearch:
    def __init__(self, model: str):
        self.model = SentenceTransformer(model)

    def generate_embedding(self, text: str):
        if not text.strip():
            raise ValueError("You must provide a text.")

        embedding: list = self.model.encode([text])

        return embedding[0]


def verify_model(model: str) -> None:
    semantic_search = SemanticSearch(model)

    print()
    print()
    print(f"Model loaded: {semantic_search.model}")
    print()
    print(f"Max sequence length: {semantic_search.model.max_seq_length}")
    print()


def embed_text(text):
    semantic_search = SemanticSearch(TRANSFORMER_MODEL)
    embedding = semantic_search.generate_embedding(text)

    print(f"Text: {text}")
    print(f"First 3 dimensions: {embedding[:3]}")
    print(f"Dimensions: {embedding.shape[0]}")
