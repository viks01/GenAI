import React from 'react';
import { Container, CssBaseline, Typography } from '@mui/material';
import RecipeRequest from './components/RecipeRequest';
import ChatBot from './components/ChatBot';
import './App.css';

function App() {
    return (
        <Container component="main" maxWidth="sm">
            <CssBaseline />
            <header className="App-header">
                <Typography variant="h3" component="h1" gutterBottom>
                    Recipe Finder
                </Typography>
            </header>
            {/* <RecipeRequest /> */}
            <ChatBot />
        </Container>
    );
}

export default App;
