import numpy as np


def run_numpy_operations():
    print("Starting NumPy operations")

    ratings = np.array([7.5, 8.1, 6.9, 9.0, 5.8])
    popularity = np.linspace(10, 100, 5)
    votes = np.arange(100, 600, 100)
    zeros = np.zeros(5)
    ones = np.ones((2, 3))

    arrays = {
        "ratings": ratings,
        "popularity": popularity,
        "votes": votes,
        "zeros": zeros,
        "ones": ones
    }

    for name, arr in arrays.items():
        print(name)
        print("shape:", arr.shape)
        print("dtype:", arr.dtype)
        print("ndim:", arr.ndim)
        print("size:", arr.size)
        print("itemsize:", arr.itemsize)
        print()

    normalized_ratings = ratings / 10
    popularity_boost = popularity * 1.15
    vote_score = ratings * votes
    rating_difference = ratings - ratings.mean()

    results = {
        "ratings_mean": float(np.mean(ratings)),
        "ratings_min": float(np.min(ratings)),
        "ratings_max": float(np.max(ratings)),
        "ratings_std": float(np.std(ratings)),
        "normalized_ratings": normalized_ratings.tolist(),
        "popularity_boost": popularity_boost.tolist(),
        "vote_score": vote_score.tolist(),
        "rating_difference": rating_difference.tolist()
    }

    print("Results:")
    print(results)

    return results


if __name__ == "__main__":
    run_numpy_operations()