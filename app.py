from flask import Flask, request, jsonify
from recommander import MovieRecommender   #  corrected import
import os

# Initialize Flask
app = Flask(__name__)

# Initialize recommender with dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "movies.csv")
recommender = MovieRecommender(csv_path)

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json()
        genre = data.get("genre")
        if not genre:
            return jsonify({"error": "Genre is required"}), 400

        results = recommender.recommend_by_genre(genre)
        return jsonify({"recommendations": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")   #  bind to all hosts for Railway
