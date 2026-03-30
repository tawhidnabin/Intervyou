from sentence_transformers import SentenceTransformer, util

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


def score_relevance(response_text, ideal_answer):
    """Compute cosine similarity between response and ideal answer. Returns 0.0–1.0."""
    if not response_text or not response_text.strip():
        return 0.5
    if not ideal_answer or not ideal_answer.strip():
        return 0.5

    model = _get_model()
    embeddings = model.encode([response_text, ideal_answer], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(max(0.0, min(1.0, similarity)), 3)
