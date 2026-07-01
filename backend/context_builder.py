def build_context(top_chunks):

    context = ""

    for result in top_chunks:

        chunk = result["chunk"]
        score = result["score"]

        context += (
            f"\n[Page {chunk['page']} | "
            f"Chunk {chunk['chunk_id']} | "
            f"Score {round(score,4)}]\n\n"
        )

        context += chunk["text"]

        context += "\n\n--------------------------------\n"

    return context
