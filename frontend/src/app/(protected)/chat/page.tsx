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

interface Message {
  id: number;
  sender: string;
  content: string;
  isMine: boolean;
}

const ChatPage: React.FC = () => {
  // 初始聊天记录（示例）
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, sender: 'Alice', content: 'Hello there!', isMine: false },
    { id: 2, sender: 'You', content: 'Hi, Alice!', isMine: true },
  ]);

  // 文本框内容
  const [inputValue, setInputValue] = useState('');

  // 发送消息
  const handleSend = () => {
    if (!inputValue.trim()) return;
    setMessages((prev) => [
      ...prev,
      {
        id: prev.length + 1,
        sender: 'You',
        content: inputValue,
        isMine: true,
      },
    ]);
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

      {/* 消息列表 */}
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

      {/* 输入框和发送按钮 */}
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
