from sentence_transformers import SentenceTransformer


class SemanticSearch:
    def __init__(self, model):
        self.model = SentenceTransformer(model)


def verify_model(model: str) -> None:
    semantic_search = SemanticSearch(model)

    print()
    print()
    print(f"Model loaded: {semantic_search.model}")
    print()
    print(f"Max sequence length: {semantic_search.model.max_seq_length}")
    print()
