import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="database")

collection = client.get_collection(
    name="enterprise_knowledge_base"
)

model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_chunks(query, top_k=1):
    query_embedding = model.encode(query)

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    print(results)

    return results