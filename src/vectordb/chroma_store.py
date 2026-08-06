import chromadb

client = chromadb.PersistentClient(path="database")

collection = client.get_or_create_collection(
    name="enterprise_knowledge_base"
)


def store_embeddings(chunks, embeddings, sources):

    # Clear old data before re-indexing
    try:
        collection.delete(ids=collection.get()["ids"])
    except:
        pass

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    metadatas = [
        {"source": source}
        for source in sources
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"\n{len(chunks)} chunks stored successfully!")