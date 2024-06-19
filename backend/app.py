from flask import Flask, request, jsonify
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import os

app = Flask(__name__)

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
pc = Pinecone(api_key='YOUR_PINECONE_API_KEY')

# Create a Pinecone index (if it doesn't exist) which stores the recipe embeddings (vectors)
index_name = "recipes-index"
if index_name not in [index.name for index in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="euclidean",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ) 
    )

index = pc.Index(index_name)


# Initialize OpenAI
client = OpenAI(api_key='YOUR_OPENAI_API_KEY')

# Function to get the embedding of a text using OpenAI
# def get_embedding(text):
#     response = openai.Embedding.create(
#         input=text,
#         model="text-embedding-ada-002"  # Specify the model
#     )
#     return response['data'][0]['embedding']

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


# Insert initial recipes into the Pinecone index
def insert_initial_recipes():
    for recipe in recipes:
        recipe_embedding = get_embedding(recipe['title']) # Here we use the recipe title as the text to get the embedding
        index.upsert([(recipe['id'], recipe_embedding)])

insert_initial_recipes()


# API section
@app.route('/api/recipes', methods=['POST'])
def get_recipes():
    data = request.get_json()
    recipe_name = data.get('recipeName')
    query_embedding = get_embedding(recipe_name)

    response = index.query(query_embedding, top_k=5)
    matches = response['matches']

    matched_recipes = []
    for match in matches:
        for recipe in recipes:
            if recipe['id'] == match['id']:
                matched_recipes.append({"title": recipe['title'], "url": recipe['url']})

    return matched_recipes

if __name__ == '__main__':
    app.run(debug=True)
