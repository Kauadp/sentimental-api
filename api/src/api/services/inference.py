import joblib
import numpy as np
from ..config import VECTORIZER_PATH, MODEL_PATH

vectorizer = joblib.load(VECTORIZER_PATH)
model = joblib.load(MODEL_PATH)

def get_text_vector(text):
    """Convert text to vector using Word2Vec average."""
    words = text.lower().split()
    vectors = []
    for word in words:
        if word in vectorizer.wv:
            vectors.append(vectorizer.wv[word])
    if vectors:
        return np.mean(vectors, axis=0)
    else:
        return np.zeros(vectorizer.vector_size)

def infer_probability(text: str) -> float:
    """Infer sentiment probability for the given text."""
    X = get_text_vector(text).reshape(1, -1)
    proba = model.predict_proba(X)[0, 1]
    return float(proba)
