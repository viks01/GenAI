import React, { useState } from 'react';
import {
    TextField, Button, CircularProgress,
    List, ListItem, ListItemText, Typography, Box, Paper
} from '@mui/material';

const ChatBot = () => {
    const [userId] = useState('user123'); // Example user ID, you can generate or fetch this dynamically
    const [userQuery, setUserQuery] = useState('');
    const [chatHistory, setChatHistory] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        setLoading(true);
        const newMessage = { sender: 'User', text: userQuery };

        // Add user query to chat history
        setChatHistory([...chatHistory, newMessage]);
        setUserQuery('');

        fetch('http://127.0.0.1:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userId, query: userQuery })
        })
        .then(response => response.json())
        .then(data => {
            const botResponse = { sender: 'Bot', text: data.response };
            setChatHistory(prevHistory => [...prevHistory, botResponse]);
            setLoading(false);
        })
        .catch(error => {
            console.error('Error:', error);
            setLoading(false);
        });
    };

    return (
        <Box>
            <Paper elevation={3} style={{ padding: '20px', maxWidth: '600px', margin: '20px auto' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Recipe ChatBot
                </Typography>
                <Box style={{ maxHeight: '400px', overflowY: 'auto', marginBottom: '20px' }}>
                    <List>
                        {chatHistory.map((message, index) => (
                            <ListItem key={index}>
                                <ListItemText
                                    primary={message.text}
                                    secondary={message.sender}
                                    style={{ textAlign: message.sender === 'User' ? 'right' : 'left' }}
                                />
                            </ListItem>
                        ))}
                    </List>
                </Box>
                <form onSubmit={handleSubmit} style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', width: '100%' }}>
                    <TextField
                        label="Type your query"
                        variant="outlined"
                        value={userQuery}
                        onChange={(e) => setUserQuery(e.target.value)}
                        style={{ marginBottom: '20px', width: '80%' }}
                        InputLabelProps={{
                            style: { color: 'grey' }, // Label color
                        }}
                        InputProps={{
                            style: { color: 'black' }, // Text color
                        }}
                    />
                    <Button type="submit" variant="contained" color="primary" disabled={loading}>
                        Send
                    </Button>
                </form>
                {loading && <CircularProgress style={{ marginTop: '20px' }} />}
            </Paper>
        </Box>
    );
};

export default ChatBot;
