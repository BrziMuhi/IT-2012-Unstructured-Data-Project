from embeddings.search_engine import keyword_search, semantic_search


def get_result_name(row):
    if hasattr(row, "name"):
        return row.name
    if hasattr(row, "title"):
        return row.title
    return "Unknown"


def reciprocal_rank_fusion(keyword_results, semantic_results, k: int = 60):
    scores = {}

    for rank, row in enumerate(keyword_results.itertuples(), start=1):
        item_name = get_result_name(row)
        scores[item_name] = scores.get(item_name, 0) + 1 / (k + rank)

    for rank, metadata in enumerate(semantic_results["metadatas"][0], start=1):
        item_name = metadata.get("name", metadata.get("title", "Unknown"))
        scores[item_name] = scores.get(item_name, 0) + 1 / (k + rank)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked


def hybrid_search(df, query: str, n_results: int = 5):
    keyword_results = keyword_search(df, query, n_results)
    semantic_results = semantic_search(query, n_results)

    fused_results = reciprocal_rank_fusion(keyword_results, semantic_results)

    return fused_results[:n_results]