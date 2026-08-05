from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):

    embeddings = model.encode(chunks)

    return embeddings


if __name__ == "__main__":

    sample_chunks = [
        "Employees receive 20 annual leave days.",
        "Passwords must be changed every 90 days.",
        "Business travel requires manager approval."
    ]

    embeddings = generate_embeddings(sample_chunks)

    print("Number of Embeddings:", len(embeddings))

    print("\nEmbedding Dimension:", len(embeddings[0]))

    print("\nFirst 10 Values of First Embedding:")

    print(embeddings[0][:10])