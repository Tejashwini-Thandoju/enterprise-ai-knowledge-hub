#import chromadb


#client = chromadb.PersistentClient(path="database")


#collection = client.get_or_create_collection(
    #name="enterprise_knowledge_base"
#)

import chromadb

client = chromadb.PersistentClient(path="database")

collection = client.get_or_create_collection(
    name="enterprise_knowledge_base"
)


def store_embeddings(chunks, embeddings):

    ids = []

    for index in range(len(chunks)):
        ids.append(f"chunk_{index}")

    collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings,
    metadatas=[
        {"source": "HR_Policy.pdf"} for _ in chunks
    ]
)

    print(f"{len(chunks)} chunks stored successfully!")


