from retriever.retriever import retrieve_chunks
from llm.groq_client import generate_answer


def main():

    print("=" * 70)
    print("Enterprise AI Knowledge Hub")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        question = input("\nAsk a question: ")

        if question.lower() == "exit":
            print("\nGoodbye!")
            break

        # Retrieve relevant chunks
        results = retrieve_chunks(question, top_k=2)

        # Build context for the LLM
        context = "\n\n".join(results["documents"][0])

        # Generate answer
        answer = generate_answer(context, question)

        print("\n" + "=" * 70)
        print("Answer:\n")
        print(answer)

        print("\nSources:")

        shown_sources = set()

        for metadata in results["metadatas"][0]:
            source = metadata["source"]

            if source not in shown_sources:
                print(f"- {source}")
                shown_sources.add(source)

        print("=" * 70)


if __name__ == "__main__":
    main()