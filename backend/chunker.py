def chunk_text(text, chunk_size=500):

    chunks = []

    for i in range(0, len(text), chunk_size):

        chunk = text[i:i + chunk_size]

        chunks.append(chunk)

    return chunks

def chunk_pages(page_data, chunk_size=500):

    all_chunks = []

    chunk_id = 1

    for page in page_data:

        page_number = page["page"]

        text = page["text"]

        chunks = chunk_text(text, chunk_size)

        for chunk in chunks:

            all_chunks.append(
                {
                    "page": page_number,
                    "chunk_id": chunk_id,
                    "text": chunk
                }
            )

            chunk_id += 1

    return all_chunks
