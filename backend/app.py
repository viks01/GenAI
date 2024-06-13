from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    recipe_name = data.get('recipeName')

    # Here you can integrate with an external API to get recipe links
    # For this example, let's assume you have a list of links
    example_links = [
        {"title": "Recipe 1", "url": "http://example.com/recipe1"},
        {"title": "Recipe 2", "url": "http://example.com/recipe2"},
        {"title": "Recipe 3", "url": "http://example.com/recipe3"}
    ]

    return example_links

if __name__ == '__main__':
    app.run(debug=True)
