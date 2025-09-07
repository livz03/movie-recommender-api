import pandas as pd

class MovieRecommender:
    def __init__(self, data_path="movies.csv"):
        # Load dataset
        self.movies = pd.read_csv(data_path)
        
        # Handle genres column safely
        if 'genres' in self.movies.columns:
            self.movies['genres'] = self.movies['genres'].apply(
                lambda x: x.split('|') if isinstance(x, str) else []
            )
        else:
            raise ValueError("Dataset must contain a 'genres' column")

    def recommend_by_genre(self, genre, n=5):
        """Recommend top-n movies based on genre"""
        results = self.movies[
            self.movies['genres'].apply(lambda x: genre in x)
        ]['title'].head(n).tolist()
        
        return results if results else [f"No movies found for genre: {genre}"]
