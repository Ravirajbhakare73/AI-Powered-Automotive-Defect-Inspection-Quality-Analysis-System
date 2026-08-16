from backend.services.rag import build_knowledge_base


def main():

    print("\nBuilding automotive knowledge base...")
    print("------------------------------------")

    count = build_knowledge_base()

    if count == 0:
        print("\nNo knowledge documents found.")
        return

    print("\nRAG knowledge base built successfully.")
    print(f"Documents indexed: {count}")
    print("Vector database: chroma_db")
    print("Collection: automotive_quality")


if __name__ == "__main__":
    main()