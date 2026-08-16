from backend.services.rag import search_knowledge


def main():

    query = (
        "A scratch has appeared on the painted "
        "vehicle body. What could be the possible "
        "causes and how should it be diagnosed?"
    )

    print("\nSearching automotive knowledge base...")
    print("----------------------------------------")

    results = search_knowledge(
        query=query,
        top_k=3
    )

    if not results:

        print("No relevant knowledge found.")
        return

    print(
        f"\nFound {len(results)} relevant documents:\n"
    )

    for index, document in enumerate(
        results,
        start=1
    ):

        print(
            f"\n========== RESULT {index} ==========\n"
        )

        print(document)


if __name__ == "__main__":
    main()