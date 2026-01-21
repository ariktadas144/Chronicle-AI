import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def cosine_similarity_score(vec1: list, vec2: list) -> float:
    return cosine_similarity([vec1], [vec2])[0][0]

def normalize_vector(vec: list) -> list:
    arr = np.array(vec)
    norm = np.linalg.norm(arr)
    return (arr / norm).tolist() if norm > 0 else vec