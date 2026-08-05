from loaders.pdf_loader import load_pdf
from chunkers.text_chunker import chunk_text
from embeddings.embedding_generator import generate_embeddings
from vectordb.chroma_store import store_embeddings


def main():
    pdf_text = load_pdf("data/raw/HR_Policy.pdf")

    chunks = chunk_text(pdf_text)

    embeddings = generate_embeddings(chunks)

    store_embeddings(chunks, embeddings)


if __name__ == "__main__":
    main()