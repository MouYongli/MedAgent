'use client';

import React, { useState } from 'react';
import {
  List,
  ListItem,
  TextField,
  Button,
  Typography,
  Divider,
  Box,
  Container,
} from '@mui/material';
import { Send as SendIcon } from '@mui/icons-material';
import axios from 'axios';

interface Message {
  id: number;
  sender: string;
  content: string;
  isMine: boolean;
}

const API_URL = "http://localhost:5000/api/chat" /* TODO: update (set in some config??) */

const ChatPage: React.FC = () => {
  // Initial chat history (example)
  const [messages, setMessages] = useState<Message[]>([]);

  // Textbox content
  const [inputValue, setInputValue] = useState('');

  // Send message
  const handleSend = async () => {
    if (!inputValue.trim()) return;

    const newMessage: Message = {
      id: messages.length + 1,
      sender: 'User', // TODO: update sender (set to concrete user of default, set in config??)
      content: inputValue,
      isMine: true
    }

    setMessages((prev) => [...prev, newMessage]);

    try {
      const response = await axios.post(API_URL, { message: inputValue })

      const systemMessage: Message = {
        id: newMessage.id + 1,
        sender: 'System',
        content: response.data.reply,
        isMine: false,
      }

      setMessages((prev) => [...prev, systemMessage]);
    } catch (error) {
      console.error('Error sending and receiving message: ', error);
    }

    setInputValue('');
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Chat with Alice
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {/* Message list */}
      <List sx={{ mb: 2, height: '60vh', overflowY: 'auto' }}>
        {messages.map((item) => (
          <ListItem
            key={item.id}
            sx={{
              display: 'flex',
              justifyContent: item.isMine ? 'flex-end' : 'flex-start',
              px: 2,
              py: 1,
            }}
          >
            <Box
              sx={{
                maxWidth: '60%',
                p: 1.5,
                borderRadius: 3,
                bgcolor: item.isMine ? 'primary.main' : 'grey.100',
                color: item.isMine ? 'white' : 'text.primary',
                wordWrap: 'break-word',
              }}
            >
              <Typography variant="body1">
                {item.content}
              </Typography>
            </Box>
          </ListItem>
        ))}
      </List>

      {/* Input box and send button */}
      <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
        <TextField
          fullWidth
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter the message..."
          size="small"
          multiline
          maxRows={4}
        />
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          onClick={handleSend}
          sx={{ minWidth: 100 }}
        >
          Send
        </Button>
      </Box>
    </Container>
  );
};

export default ChatPage;
