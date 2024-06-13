import React from 'react';
import './App.css';
import RecipeRequest from './components/RecipeRequest';

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Recipe Finder</h1>
                <RecipeRequest />
            </header>
        </div>
    );
}

export default App;
