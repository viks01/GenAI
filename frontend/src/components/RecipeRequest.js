import React, { useState } from 'react';
import {
    TextField, Button, CircularProgress,
    List, ListItem, ListItemText, Typography, Box
} from '@mui/material';

const RecipeRequest = () => {
    const [recipeName, setRecipeName] = useState('');
    const [links, setLinks] = useState([]);
    const [recipeDetails, setRecipeDetails] = useState([]);
    const [loading, setLoading] = useState(false);
    const [detailsLoading, setDetailsLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        setDetailsLoading(true);
        
        fetch('http://127.0.0.1:5000/api/recipes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipeName })
        })
        .then(response => response.json())
        .then(data => {
            setLinks(data);
            setLoading(false);
        })
        .catch(error => {
            console.error('Error:', error);
            setLoading(false);
        });

        fetch('http://127.0.0.1:5000/api/recipe_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ recipeName })
        })
        .then(response => response.json())
        .then(data => {
            setRecipeDetails(data);
            setDetailsLoading(false);
        })
        .catch(error => {
            console.error('Error:', error);
            setDetailsLoading(false);
        });
    };

    return (
        <Box>
            <form onSubmit={handleSubmit} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', width: '100%' }}>
                <TextField
                    label="Type your query"
                    variant="outlined"
                    value={recipeName}
                    onChange={(e) => setRecipeName(e.target.value)}
                    style={{ marginBottom: '20px', width: '80%' }}
                    InputLabelProps={{
                        style: { color: 'grey' }, // Label color
                    }}
                    InputProps={{
                        style: { color: 'black' }, // Text color
                    }}
                />
                <Button type="submit" variant="contained" color="primary">
                    Search
                </Button>
            </form>
            {loading && <CircularProgress style={{ marginTop: '20px' }} />}
            <Box className="results-section">
                <Typography variant="h5" component="h2" gutterBottom>
                    Recipe Links
                </Typography>
                <List>
                    {links.map((link, index) => (
                        <ListItem key={index} component="a" href={link.url} target="_blank" rel="noopener noreferrer" button>
                            <ListItemText primary={link.title} style={{ color: 'black' }} />
                        </ListItem>
                    ))}
                </List>
                <br />
                <Typography variant="h5" component="h2" gutterBottom>
                    Recipe Details
                </Typography>
                {detailsLoading ? (
                    <CircularProgress style={{ marginTop: '20px' }} />
                ) : (
                    <Typography variant="body1" style={{ color: 'black' }}>{recipeDetails.response}</Typography>
                )}
            </Box>
        </Box>
    );
};

export default RecipeRequest;
