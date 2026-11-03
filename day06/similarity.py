"""Cosine similarity between embedding vectors (Day 06 retrieval)."""

import numpy as np


def cosine_similarity(vector1, vector2):
    """Return cosine similarity: 1 = same direction, 0 = orthogonal."""
    v1 = np.array(vector1)
    v2 = np.array(vector2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
