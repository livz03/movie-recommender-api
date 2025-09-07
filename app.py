from flask import Flask, request, jsonify
from recommender import MovieRecommender
import os

# Initialize Flask
app = Flask(__name__)

# Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "movies.csv")
recommender = MovieRecommender(csv_path)

@app.route("/recommend_by_genre", methods=["POST"])
def recommend_by_genre():
    try:
        data = request.get_json()
        genre = data.get("genre")
        if not genre:
            return jsonify({"error": "Genre is required"}), 400

        results = recommender.recommend_by_genre(genre)
        return jsonify({"recommendations": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recommend_by_movie", methods=["POST"])
def recommend_by_movie():
    try:
        data = request.get_json()
        title = data.get("title")
        if not title:
            return jsonify({"error": "Movie title is required"}), 400

        results = recommender.recommend_for_movie(title)
        return jsonify({"recommendations": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
