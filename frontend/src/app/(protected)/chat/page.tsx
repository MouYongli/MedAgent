"use client";

import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  List,
  ListItem,
  TextField,
  Button,
  Box,
  Divider,
} from "@mui/material";
import { Send as SendIcon } from "@mui/icons-material";
import { useRouter, useSearchParams } from "next/navigation";
import axios from "axios";

interface Message {
  id: number;
  sender: string;
  content: string;
  isMine: boolean;
}

const API_URL = "http://localhost:5000/api/chat";

const ChatPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const searchParams = useSearchParams();
  const router = useRouter();
  const conversationId = searchParams.get("conversation_id");

  useEffect(() => {
    if (!conversationId) {
      router.push("/chat/systemSelection");
      return;
    }

    const fetchInitialMessage = async () => {
      try {
        const response = await axios.post(`${API_URL}/init`, {
          generator_name: "simple",
          parameters: {},
        });
        setMessages([{ id: 1, sender: "System", content: response.data.message, isMine: false }]);
      } catch (error) {
        console.error("Error initializing conversation:", error);
      }
    };

    fetchInitialMessage();
  }, [conversationId, router]);

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleSend = async () => {
    if (!inputValue.trim() || !conversationId) return;

    const userMessage: Message = {
      id: messages.length + 1,
      sender: "User",
      content: inputValue,
      isMine: true,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post(`${API_URL}/message`, {
        conversation_id: conversationId,
        message: inputValue,
      });

      const systemMessage: Message = {
        id: userMessage.id + 1,
        sender: "System",
        content: response.data.message,
        isMine: false,
      };

      setMessages((prev) => [...prev, systemMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
    }

    setInputValue("");
  };

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Chat
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {/* Message List */}
      <List sx={{ mb: 2, height: "60vh", overflowY: "auto" }}>
        {messages.map((item) => (
          <ListItem
            key={item.id}
            sx={{
              display: "flex",
              justifyContent: item.isMine ? "flex-end" : "flex-start",
              px: 2,
              py: 1,
            }}
          >
            <Box
              sx={{
                maxWidth: "60%",
                p: 1.5,
                borderRadius: 3,
                bgcolor: item.isMine ? "primary.main" : "grey.100",
                color: item.isMine ? "white" : "text.primary",
                wordWrap: "break-word",
              }}
            >
              <Typography variant="body1">{item.content}</Typography>
            </Box>
          </ListItem>
        ))}
      </List>

      {/* Input Box and Send Button */}
      <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
        <TextField
          fullWidth
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter your message..."
          size="small"
          multiline
          maxRows={4}
        />
        <Button variant="contained" endIcon={<SendIcon />} onClick={handleSend} sx={{ minWidth: 100 }}>
          Send
        </Button>
      </Box>
    </Container>
  );
};

export default ChatPage;
