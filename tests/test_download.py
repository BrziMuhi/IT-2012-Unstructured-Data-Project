import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.image_processing.downloader import fetch_popular_movies, download_movie_posters

movies = fetch_popular_movies(pages=1)
print(f"Fetched {len(movies)} movies")

results = download_movie_posters(movies[:5], dest_dir="data/raw/images")

if results:
    for r in results:
        print(r["title"], "->", r["local_path"])
else:
    print("No posters were downloaded.")