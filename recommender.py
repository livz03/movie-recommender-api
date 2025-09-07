import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class MovieRecommender:
    def __init__(self, dataset_path):
        self.movies = pd.read_csv(dataset_path)

        # Create TF-IDF matrix based on genres
        tfidf = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = tfidf.fit_transform(self.movies["genres"].fillna(""))

        # Similarity matrix
        self.similarity_matrix = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)

    def recommend_by_genre(self, genre, top_n=5):
        """Filter movies by genre"""
        filtered = self.movies[self.movies["genres"].str.contains(genre, case=False, na=False)]
        return filtered["title"].head(top_n).tolist()

    def recommend_for_movie(self, title, top_n=5):
        """Recommend movies similar to a given movie"""
        if title not in self.movies["title"].values:
            return []

        idx = self.movies[self.movies["title"] == title].index[0]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # skip itself
        movie_indices = [i[0] for i in sim_scores]
        return self.movies.iloc[movie_indices]["title"].tolist()
