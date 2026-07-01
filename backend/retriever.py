from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def calculate_similarity(question_embedding, chunk_embedding):

    score = cosine_similarity(
        question_embedding.reshape(1, -1),
        chunk_embedding.reshape(1, -1)
    )

    return score[0][0]  

def retrieve_best_chunk(
    question_embedding,
    chunks
):

    best_score = -1
    best_chunk = None

    for chunk in chunks:

        score = calculate_similarity(
            question_embedding,
            chunk["embedding"]
        )

        if score > best_score:

            best_score = score
            best_chunk = chunk

    return best_chunk, best_score

def retrieve_top_k_chunks(
    question_embedding,
    chunks,
    k=3
):

    results = []

    for chunk in chunks:

        score = calculate_similarity(
            question_embedding,
            chunk["embedding"]
        )

        results.append(
            {
                "chunk": chunk,
                "score": score
            }
        )

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:k]