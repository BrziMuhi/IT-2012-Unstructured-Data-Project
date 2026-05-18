import pandas as pd

from embeddings.chroma_store import query_chroma


def semantic_search(query: str, n_results: int = 5, where: dict | None = None):
    return query_chroma(query_text=query, n_results=n_results, where=where)


def keyword_search(df: pd.DataFrame, query: str, n_results: int = 5):
    query = query.lower()

    text_columns = ["name", "formatted_address", "city", "country", "categories"]
    existing_columns = [col for col in text_columns if col in df.columns]

    mask = False

    for col in existing_columns:
        mask = mask | df[col].fillna("").astype(str).str.lower().str.contains(query, regex=False)

    results = df[mask].head(n_results)

    return results


def compare_search(df: pd.DataFrame, query: str, n_results: int = 5):
    print("KEYWORD SEARCH")
    print(keyword_search(df, query, n_results))

    print("\nSEMANTIC SEARCH")
    semantic_results = semantic_search(query, n_results)

    for metadata, distance in zip(
        semantic_results["metadatas"][0],
        semantic_results["distances"][0]
    ):
        print(metadata.get("title", metadata.get("name", "Unknown")), "| distance:", distance)