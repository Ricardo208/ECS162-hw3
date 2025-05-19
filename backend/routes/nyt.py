from flask import Blueprint, jsonify  # reference - https://flask.palletsprojects.com/en/2.3.x/blueprints/
import requests  # reference - https://realpython.com/python-requests/
import os

nyt_bp = Blueprint('nyt', __name__)  # reference - https://flask.palletsprojects.com/en/2.3.x/blueprints/

@nyt_bp.route('/api/nyt')
def get_local_stories():
    api_key = os.getenv('NYT_API_KEY')  # reference - https://12factor.net/config
    if not api_key:
        return jsonify({"error": "Missing NYT API key"}), 500

    query = "Davis Sacramento"
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={query}&api-key={api_key}"  # reference - https://developer.nytimes.com/docs/articlesearch-product/1/overview

    try:
        response = requests.get(url)  # reference - https://realpython.com/python-requests/
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
