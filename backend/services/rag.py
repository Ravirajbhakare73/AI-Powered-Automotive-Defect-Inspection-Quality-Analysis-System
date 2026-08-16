import os

import chromadb

from sentence_transformers import (
    SentenceTransformer
)


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)


KNOWLEDGE_DIR = os.path.join(
    BASE_DIR,
    "knowledge"
)


CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)


embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


client = chromadb.PersistentClient(
    path=CHROMA_DIR
)


collection = client.get_or_create_collection(
    name="automotive_quality"
)


def build_knowledge_base():

    documents = []
    ids = []

    for filename in sorted(
        os.listdir(KNOWLEDGE_DIR)
    ):

        if not filename.endswith(".md"):
            continue

        file_path = os.path.join(
            KNOWLEDGE_DIR,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        if not content.strip():
            continue

        documents.append(content)
        ids.append(filename)

    if not documents:
        return 0

    embeddings = (
        embedding_model
        .encode(documents)
        .tolist()
    )

    collection.upsert(
        documents=documents,
        embeddings=embeddings,
        ids=ids
    )

    return len(documents)


def search_knowledge(
    query,
    top_k=3
):

    query_embedding = (
        embedding_model
        .encode([query])
        .tolist()
    )

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    documents = results.get(
        "documents",
        []
    )

    if not documents:
        return []

    return documents[0]