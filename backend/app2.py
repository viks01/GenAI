from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Stored recipes
recipes = [
    {"id": "1", "title": "Dal Makhani", "url": "https://hebbarskitchen.com/punjabi-dal-makhani-recipe/"},
    {"id": "2", "title": "Palak Paneer", "url": "https://hebbarskitchen.com/palak-paneer-recipe-restaurant-style/"},
    {"id": "3", "title": "Chole Bhature", "url": "https://hebbarskitchen.com/chole-bhature-recipe-chana-bhatura/"},
    {"id": "4", "title": "Paneer Butter Masala", "url": "https://hebbarskitchen.com/paneer-butter-masala-recipe/"},
    {"id": "5", "title": "Veg Momos", "url": "https://hebbarskitchen.com/veg-momos-recipe-momos-ki-recipe/"},
    {"id": "6", "title": "Pav Bhaji", "url": "https://hebbarskitchen.com/easy-mumbai-style-pav-bhaji-recipe/"},
    {"id": "7", "title": "Veg Biryani", "url": "https://hebbarskitchen.com/veg-biryani-cooker-vegetable-biryani/"},
    {"id": "8", "title": "Masala Dosa", "url": "https://hebbarskitchen.com/masala-dosa-recipe-crispy-masale-dose/"},
    {"id": "9", "title": "Puliyogare", "url": "https://hebbarskitchen.com/puliyogare-gojju-recipe-tamarind-rice/"},
    {"id": "10", "title": "Rava Idli", "url": "https://hebbarskitchen.com/rava-idli-recipe-instant-semolina-idli/"}
]


# Initialize Pinecone
pc = Pinecone(api_key='eee99a89-2cf3-442f-9681-921a32023c0b')

index_name = "recipes-index2"
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,  # Adjust the dimension according to SentenceTransformer model
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)


# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can choose a different model

def get_embedding(text):
    return model.encode(text).tolist()


# Insert initial recipes into Pinecone
def insert_initial_recipes():
    for recipe in recipes:
        text_for_embedding = f"{recipe['title']} {recipe['url']}"
        recipe_embedding = get_embedding(text_for_embedding)
        index.upsert([(recipe['id'], recipe_embedding)])

insert_initial_recipes()


# API section
@app.route('/api/recipes', methods=['POST'])
@cross_origin()
def get_recipes():
    data = request.get_json()
    recipe_name = data.get('recipeName')
    query_embedding = get_embedding(recipe_name)

    response = index.query(vector=query_embedding, top_k=5)
    matches = response['matches']

    matched_recipes = []
    for match in matches:
        for recipe in recipes:
            if recipe['id'] == match['id']:
                matched_recipes.append({"title": recipe['title'], "url": recipe['url']})

    return jsonify(matched_recipes)

if __name__ == '__main__':
    insert_initial_recipes()
    app.run(debug=True)
