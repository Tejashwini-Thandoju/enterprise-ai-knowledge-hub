from retriever.retriever import retrieve_chunks


def main():

    question = input("Ask a question: ")

    results = retrieve_chunks(question)

    print("\nRetrieved Chunks:\n")

    for i in range(len(results["documents"][0])):

        print("=" * 60)

        print(f"Result {i + 1}")

        print()

        print(
            "Source Document:",
            results["metadatas"][0][i]["source"]
        )

        print(
            "Distance:",
            round(results["distances"][0][i], 4)
        )

        print()

        print(results["documents"][0][i])

        print("=" * 60)


if __name__ == "__main__":
    main()


