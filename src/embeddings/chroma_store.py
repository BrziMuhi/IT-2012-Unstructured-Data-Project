import os
import chromadb
from chromadb.config import Settings

from embeddings.embedder import combine_movie_text, generate_embeddings


CHROMA_PATH = "data/embeddings/chroma_db"
COLLECTION_NAME = "movies"


def get_chroma_client():
    os.makedirs(CHROMA_PATH, exist_ok=True)

    return chromadb.PersistentClient(
        path=CHROMA_PATH,
        settings=Settings(anonymized_telemetry=False)
    )


def get_or_create_collection(reset: bool = False):
    client = get_chroma_client()

    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )


def prepare_metadata(row):
    return {
        "title": str(row.get("title", "")),
        "genre": str(row.get("primary_genre", row.get("genre", ""))),
        "release_year": int(row.get("release_year", 0)) if str(row.get("release_year", "")).isdigit() else 0,
        "language": str(row.get("original_language", "")),
        "rating": float(row.get("vote_average", 0) or 0),
        "revenue": float(row.get("revenue_usd", row.get("revenue", 0)) or 0)
    }


def add_movies_to_chroma(df, reset: bool = False):
    collection = get_or_create_collection(reset=reset)

    documents = []
    metadatas = []
    ids = []

    for index, row in df.iterrows():
        movie_id = str(row.get("id", row.get("_id", index)))
        text = combine_movie_text(row)

        documents.append(text)
        metadatas.append(prepare_metadata(row))
        ids.append(movie_id)

    embeddings = generate_embeddings(documents)

    collection.add(
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids
    )

    print(f"Added {len(documents)} movies to ChromaDB")
    return collection


def query_chroma(query_text: str, n_results: int = 5, where: dict | None = None):
    collection = get_or_create_collection()

    query_embedding = generate_embeddings([query_text])

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results,
        where=where
    )

    return results

def query_chroma_multi(query_texts: list[str], n_results: int = 5, where: dict | None = None):
    collection = get_or_create_collection()

    query_embeddings = generate_embeddings(query_texts)

    results = collection.query(
        query_embeddings=query_embeddings.tolist(),
        n_results=n_results,
        where=where
    )

    return results