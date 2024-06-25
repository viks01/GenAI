from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from transformers import pipeline
from langchain_openai import OpenAIEmbeddings, OpenAI
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

# Function to delete an index if it exists
def delete_index_if_exists(index_name):
    try:
        if index_name in [index.name for index in pc.list_indexes()]:
            pc.delete_index(index_name)
            print(f"Index '{index_name}' deleted successfully.")
        else:
            print(f"Index '{index_name}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to delete index '{index_name}': {e}")

index_name = "recipes-index4"
delete_index_if_exists(index_name)
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
    embedding = model.encode(text).tolist()
    return embedding


# Initialize OpenAI model
# openai.api_key = os.getenv('OPENAI_API_KEY')
# embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")
# language_model = OpenAI(model="gpt-3.5-turbo")

# def get_embedding(text):
#     return embeddings_model.embed_query(text)


# Initialize Hugging Face model
generator = pipeline('text-generation', model='gpt2')


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
    
    try:
        response = index.query(vector=query_embedding, top_k=5)
        matches = response['matches']
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return jsonify({"error": "Error querying Pinecone"}), 500

    matched_recipes = []
    for match in matches:
        for recipe in recipes:
            if recipe['id'] == match['id']:
                matched_recipes.append({"title": recipe['title'], "url": recipe['url']})

    return jsonify(matched_recipes)


@app.route('/api/recipe_details', methods=['POST'])
@cross_origin()
def get_recipe_details():
    data = request.get_json()
    recipe_name = data.get('recipeName')
    query_embedding = get_embedding(recipe_name)

    try:
        response = index.query(vector=query_embedding, top_k=1)
        matches = response['matches']
    except Exception as e:
        print(f"Error querying Pinecone: {e}")
        return jsonify({"error": "Error querying Pinecone"}), 500

    if matches:
        recipe_id = matches[0]['id']
        for recipe in recipes:
            if recipe['id'] == recipe_id:
                # Use GPT-3.5 to generate a detailed response
                context = f"Recipe: {recipe['title']} - {recipe['url']}"
                prompt = f"{context}\n\nCould you give me the steps to make {recipe_name}?"
                # completion = language_model(prompt)
                # return jsonify({"response": completion['choices'][0]['text']})
                completion = generator(prompt, max_length=1500)
                return jsonify({"response": completion[0]['generated_text']})
    return jsonify({"response": "Recipe not found."})


if __name__ == '__main__':
    app.run(debug=True)
