from sentence_transformers import SentenceTransformer, util

from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

from typing import List

__sentence_transformer = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

def get_similarity_measure(source_sentence : str, sentences : List[str]):
    model = __sentence_transformer
    source_embedding = model.encode([source_sentence])
    sentence_embeddings = model.encode(sentences)
    similarity_measures = cosine_similarity([source_embedding], sentence_embeddings)

    return np.argmax(similarity_measures[0])