import os

from loaders.pdf_loader import load_pdf
from chunkers.text_chunker import chunk_text
from embeddings.embedding_generator import generate_embeddings
from vectordb.chroma_store import store_embeddings


def main():

    pdf_folder = "data/raw"

    all_chunks = []
    all_embeddings = []
    all_sources = []

    for file_name in os.listdir(pdf_folder):

        if file_name.endswith(".pdf"):

            pdf_path = os.path.join(pdf_folder, file_name)

            print(f"\nLoading {file_name}...")

            pdf_text = load_pdf(pdf_path)

            chunks = chunk_text(pdf_text)

            print(f"{file_name} -> {len(chunks)} chunks")

            embeddings = generate_embeddings(chunks)

            all_chunks.extend(chunks)
            all_embeddings.extend(embeddings)
            all_sources.extend([file_name] * len(chunks))

    store_embeddings(
        all_chunks,
        all_embeddings,
        all_sources
    )


if __name__ == "__main__":
    main()