import React, { useState } from 'react';

const RecipeRequest = () => {
    const [recipeName, setRecipeName] = useState('');
    const [links, setLinks] = useState([]);
    const [recipeDetails, setRecipeDetails] = useState([]);

    const handleSubmit = (e) => {
        e.preventDefault();
        
        fetch('http://127.0.0.1:5000/api/recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipeName })
        })
        .then(response => response.json())
        .then(data => setLinks(data))
        .catch(error => console.error('Error:', error));

        fetch('http://127.0.0.1:5000/api/recipe_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipeName })
        })
        .then(response => response.json())
        .then(data => setRecipeDetails(data))
        .catch(error => console.error('Error:', error));
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    value={recipeName}
                    onChange={(e) => setRecipeName(e.target.value)}
                    placeholder="Enter recipe name"
                />
                <button type="submit">Search</button>
            </form>
            <div>
                <h2>Recipe Links</h2>
                <ul>
                    {links.map((link, index) => (
                        <li key={index}>
                            <a href={link.url} target="_blank" rel="noopener noreferrer">
                                {link.title}
                            </a>
                        </li>
                    ))}
                </ul>
                <br />
                <h2>Recipe Details</h2>
                <p>{recipeDetails.response}</p>
            </div>
        </div>
    );
};

export default RecipeRequest;
