import pandas as pd
from sentence_transformers import SentenceTransformer


_MODEL = None


def get_model(model_name: str = "all-MiniLM-L6-v2"):
    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer(model_name)

    return _MODEL


def combine_movie_text(row) -> str:
    title = str(row.get("title", ""))
    overview = str(row.get("overview", ""))
    genre = str(row.get("primary_genre", row.get("genre", row.get("genres", ""))))

    return f"Title: {title}. Genre: {genre}. Overview: {overview}"


def prepare_texts(df: pd.DataFrame) -> list[str]:
    return df.apply(combine_movie_text, axis=1).tolist()


def generate_embeddings(texts: list[str], normalize: bool = True):
    model = get_model()

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=normalize,
        show_progress_bar=True
    )

    return embeddings


def generate_movie_embeddings(df: pd.DataFrame):
    texts = prepare_texts(df)
    embeddings = generate_embeddings(texts)

    return texts, embeddings