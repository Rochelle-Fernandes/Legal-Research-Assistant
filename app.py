import streamlit as st

from backend.pdf_parser import (
    get_page_count,
    get_first_page_text,
    extract_all_pages,
    is_scanned_pdf
)

from backend.chunker import chunk_pages
from backend.embeddings import get_embedding
from backend.retriever import retrieve_top_k_chunks
from backend.context_builder import build_context
from backend.llm import generate_answer


st.set_page_config(
    page_title="Legal Research Assistant",
    layout="wide"
)

st.title("⚖️ Legal Research Assistant")

uploaded_file = st.file_uploader(
    "Upload a legal PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success("PDF uploaded successfully!")

    st.write("**Filename:**", uploaded_file.name)
    st.write("**Type:**", uploaded_file.type)
    st.write("**Size:**", uploaded_file.size, "bytes")

    # ---------------- PDF Information ----------------

    page_count = get_page_count(uploaded_file)

    st.write("**Pages:**", page_count)

    # ---------------- PDF Type ----------------

    st.subheader("Document Type")

    if is_scanned_pdf(uploaded_file):

        st.warning(
            "This appears to be a scanned PDF.\n\n"
            "OCR support will be added in a future version."
        )

        st.stop()

    else:

        st.success("This appears to be a digital PDF.")

    # ---------------- First Page Preview ----------------

    first_page_text = get_first_page_text(uploaded_file)

    st.subheader("First Page Preview")

    if first_page_text.strip():

        st.text(first_page_text[:1000])

    else:

        st.warning("No text found on Page 1.")

    # ---------------- Page Extraction ----------------

    all_pages = extract_all_pages(uploaded_file)

    st.subheader("Page-wise Extraction")

    for page_data in all_pages:

        with st.expander(f"Page {page_data['page']}"):

            st.text(page_data["text"])

    # ---------------- Chunking ----------------

    chunks = chunk_pages(
        all_pages,
        chunk_size=500
    )

    st.subheader("Chunk Statistics")

    st.write("Total Chunks:", len(chunks))

    # ---------------- Embeddings ----------------

    with st.spinner("Generating embeddings..."):

        for chunk in chunks:

            chunk["embedding"] = get_embedding(
                chunk["text"]
            )

    st.success("Embeddings generated successfully!")

    # ---------------- Question ----------------

    st.subheader("Ask Questions")

    question = st.text_input(
        "Ask a question about the document"
    )

    if question and not question.strip():

        st.warning("Please enter a valid question.")

        st.stop()

    # ---------------- Retrieval ----------------

    if question:

        with st.spinner("Searching relevant context..."):

            question_embedding = get_embedding(question)

            top_chunks = retrieve_top_k_chunks(
                question_embedding,
                chunks,
                k=3
            )

        if len(top_chunks) == 0:

            st.error("No relevant information found.")

            st.stop()

        context = build_context(top_chunks)

        # ---------------- Context ----------------

        with st.expander("Context Sent To LLM"):

            st.text(context)

        # ---------------- LLM ----------------

        with st.spinner("Generating answer..."):

            answer = generate_answer(
                context,
                question
            )

        st.success("Answer generated successfully!")

        st.subheader("Answer")

        st.write(answer)

        # ---------------- Retrieved Chunks ----------------

        st.subheader("Retrieved Chunks")

        for result in top_chunks:

            chunk = result["chunk"]

            st.markdown("---")

            st.write(
                f"**Similarity Score:** {result['score']:.4f}"
            )

            st.write(
                f"**Page:** {chunk['page']}"
            )

            st.write(
                f"**Chunk ID:** {chunk['chunk_id']}"
            )

            st.text(chunk["text"])