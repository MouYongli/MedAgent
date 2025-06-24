'use client';

import React, { useEffect, useState } from 'react';
import {
  List,
  ListItem,
  TextField,
  Button,
  Typography,
  Divider,
  Box,
  Container,
  LinearProgress, // Change from CircularProgress to LinearProgress
  Drawer,
  IconButton,
} from '@mui/material';
import { Bookmark, BookOnline, Done, DoneAllRounded, Send as SendIcon } from '@mui/icons-material';
import CloseIcon from '@mui/icons-material/Close';
import { v4 as uuidv4 } from 'uuid';
import stubData from './stub_data.json';
import ThumbUpAltOutlinedIcon from '@mui/icons-material/ThumbUpAltOutlined';
import ThumbDownAltOutlinedIcon from '@mui/icons-material/ThumbDownAltOutlined';

interface Message {
  id: string;
  sender: string;
  content: string;
  isUser: boolean;
}

const likertOptions = [
  { value: 'very_inconsistent', label: 'Very inconsistent' },
  { value: 'somewhat_inconsistent', label: 'Somewhat inconsistent' },
  { value: 'somewhat_consistent', label: 'Somewhat consistent' },
  { value: 'very_consistent', label: 'Very consistent' },
];

function parseMessage(content: string) {
  // Split by newline first to preserve line breaks
  return content.split('\n').map((line, i) => {
    // Replace **bold** with <strong>
    const parts = line.split(/(\*\*[^*]+\*\*)/g);
    return (
      <React.Fragment key={i}>
        {parts.map((part, j) =>
          part.startsWith('**') && part.endsWith('**') ? (
            <strong key={j}>{part.slice(2, -2)}</strong>
          ) : (
            <React.Fragment key={j}>{part}</React.Fragment>
          )
        )}
        {i < content.split('\n').length - 1 && <br />}
      </React.Fragment>
    );
  });
}
const ChatPage: React.FC = () => {
  // Initial chat messages (example)
  const [messages, setMessages] = useState<Message[]>([
    { id: uuidv4(), sender: 'Alice', content: 'Hello there! I am an Oral Maxillofacial Surgery assistant. Happy to help!', isUser: false },
  ]);

  // Text field content
  const [inputValue, setInputValue] = useState('');
  const [stubIndex, setStubIndex] = useState(0);
  const [loading, setLoading] = useState(false); // Add loading state
  const [selectedLikert, setSelectedLikert] = useState<string | null>(null);
  const [sourcePanelOpen, setSourcePanelOpen] = useState(false);
  const [chunks, setChunks] = useState<any[]>([]); // Add this state for chunks
  const [chunkFeedback, setChunkFeedback] = useState<{ [key: number]: 'up' | 'down' | null }>({});
  const [ratingComplete, setRatingComplete] = useState(false);
  const [streamingComplete, setStreamingComplete] = useState(false);
  // Send message
  const handleSend = async () => {
    if (!inputValue.trim()) return;
    setMessages((prev) => [
      ...prev,
      {
        id: uuidv4(),
        sender: 'You',
        content: inputValue,
        isUser: true,
      },
    ]);
    setInputValue('');
    setLoading(true);

    // Prepare for streaming response
    const assistantId = uuidv4();
    setMessages((prev) => [
      ...prev,
      {
        id: assistantId,
        sender: 'Alice',
        content: '',
        isUser: false,
      },
    ]);
    setChunkFeedback({});
    setRatingComplete(false);
    setSelectedLikert(null);
    setStreamingComplete(false);
    let localStreamingComplete = false;
    try {
      
      const response = await fetch('http://localhost:8000/api/chat/send/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sender: "anonymous monkey",content: inputValue }),
      });
      
      if (!response.body) throw new Error('No response body');
      setLoading(false);
      
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      
      let accumulated = '';
      
      while (!localStreamingComplete) {
        const { value, done: doneReading } = await reader.read();
        if (doneReading) {
          localStreamingComplete = true;
          setStreamingComplete(true);
          break;
        }
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n').filter(Boolean);
        
        for (const line of lines) {
          let data;
          try {
            data = JSON.parse(line);
          } catch {
            continue;
          }
          if (data.content !== undefined) {
            accumulated += data.content;
            
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantId
                  ? { ...msg, content: accumulated }
                  : msg
              )
            );
          }
          if (data.done) {
            setChunks(data.chunks ?? []);
            setStubIndex((prev) => prev + 1);
            localStreamingComplete = true;
            setStreamingComplete(true);
            break;
          }
          
        }
      }
      // console.log("Accumulated content:", accumulated);
    } catch (err) {
      console.log('Error during streaming:', err);
      
    }
    
    
    setLoading(false);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const handleSourceView = () => {
    setSourcePanelOpen(true);
  };

  const handleCloseSourcePanel = () => {
    setSourcePanelOpen(false);
  };

  const storeStudyData = () => {
    
    const userData = { 
      "user_id": "user123", // Replace with actual user ID
      "id": messages[messages.length - 1].id,
      "user_message": messages[messages.length - 2].content,
      "system_message": messages[messages.length - 1].content,
      "likert_rating": selectedLikert,
      "chunk_feedback": chunkFeedback,
    };
    console.log("Implement data storage logic")
    console.log("User Data:", userData);
    setRatingComplete(true);

  }

 

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Chat with Alice
      </Typography>
      <Divider sx={{ mb: 3 }} />

      {/* Message list */}
      <List sx={{ mb: 2, height: '60vh', overflowY: 'auto' }}>
        {/* Render all messages except the last one if the last is not a user message */}
        {(messages.length > 1 && !messages[messages.length - 1].isUser
          ? messages.slice(0, -1)
          : messages
        ).map((item) => (
          <ListItem
            key={item.id}
            sx={{
              display: 'flex',
              justifyContent: item.isUser ? 'flex-end' : 'flex-start',
              px: 2,
              py: 1,
            }}
          >
            <Box
              sx={{
                maxWidth: '60%',
                p: 1.5,
                borderRadius: 3,
                bgcolor: item.isUser ? 'primary.main' : 'grey.100',
                color: item.isUser ? 'white' : 'text.primary',
                wordWrap: 'break-word',
              }}
            >
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {parseMessage(item.content)}
              </Typography>
            </Box>
          </ListItem>
        ))}
        {loading && (
          <ListItem
            sx={{
              display: 'flex',
              justifyContent: 'flex-start',
              px: 2,
              py: 1,
            }}
          >
            <Box sx={{ width: '60%' }}>
              <LinearProgress />
            </Box>
          </ListItem>
        )}
        {/* If the last message is not a user message, render it after the loader */}
        {!loading && messages.length > 1 && !messages[messages.length - 1].isUser && (
          <>
            <ListItem
              key={messages[messages.length - 1].id}
              sx={{
                display: 'flex',
                justifyContent: 'flex-start',
                px: 2,
                py: 1,
              }}
            >
              <Box
                sx={{
                  maxWidth: '60%',
                  p: 1.5,
                  borderRadius: 3,
                  bgcolor: 'grey.100',
                  color: 'text.primary',
                  wordWrap: 'break-word',
                }}
              >
                <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                  {parseMessage(messages[messages.length - 1].content)}
                </Typography>
              </Box>
              
            </ListItem>
            {!streamingComplete && (
                <ListItem
                  sx={{
                    display: 'flex',
                    justifyContent: 'flex-start',
                    px: 2,
                    py: 1,
                  }}
                >
                  <Box sx={{ width: '60%' }}>
                    <LinearProgress />
                  </Box>
                </ListItem>
              )}
            {streamingComplete && (<ListItem
              sx={{
                display: 'flex',
                justifyContent: 'flex-start',
                px: 2,
                py: 0,
                flexDirection: 'column',
                alignItems: 'flex-start',
              }}
            >
              <Button variant="outlined" endIcon={<Bookmark />} onClick={handleSourceView} size="small" sx={{ mb: 1 }}>
                Sources
              </Button>
              <Box sx={{ height: 8 }} /> {/* Add a small space below the Sources button */}
              {/* Likert scale */}
              <Typography variant="subtitle2" align="center" sx={{ mb: 1, fontWeight: 'normal', fontSize: '1rem' }}>
                Rate my answer:
              </Typography>
              <Box sx={{ display: 'flex', gap: 4, mt: 1 }}>
                {likertOptions.map((option) => (
                  <Box key={option.value} sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <Button
                      variant={selectedLikert === option.value ? 'contained' : 'outlined'}
                      size="small"
                      onClick={() => setSelectedLikert(option.value)}
                      sx={{
                        minWidth: 0,
                        width: 20,
                        height: 20,
                        borderRadius: '50%',
                        p: 0,
                        mb: 0.5,
                        bgcolor: selectedLikert === option.value ? 'primary.main' : 'background.paper',
                        color: selectedLikert === option.value ? 'white' : 'text.primary',
                        borderColor: selectedLikert === option.value ? 'primary.main' : undefined,
                        transition: 'all 0.2s',
                      }}
                    />
                    <Typography
                      variant="subtitle2"
                      align="center"
                      sx={{ width: 80, fontSize: '1rem', mt: 0.5 }}
                    >
                      {option.label}
                    </Typography>
                  </Box>
                ))}
              </Box>
              <Button
                variant="contained"
                color="primary"
                onClick={storeStudyData}
                sx={{ mt: 2, width: '25%' }}
                disabled={!selectedLikert || ratingComplete || Object.keys(chunkFeedback).length === 0}
                endIcon={Object.keys(chunkFeedback).length !== 0 && selectedLikert ? (ratingComplete ?  <DoneAllRounded/> :  <Done />) : null }
              >
                {Object.keys(chunkFeedback).length !== 0 && selectedLikert ? (ratingComplete ?  'Completed' :  'Complete Rating') : 'Rate'}
              </Button>
            </ListItem>)}
          </>
        )}
      </List>

      {/* Side panel for sources */}
      <Drawer
        anchor="right"
        open={sourcePanelOpen}
        onClose={handleCloseSourcePanel}
        PaperProps={{ sx: { width: 350 } }}
      >
        <Box sx={{ display: 'flex', alignItems: 'center', p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Rate the Sources
          </Typography>
          <IconButton onClick={handleCloseSourcePanel}>
            <CloseIcon />
          </IconButton>
        </Box>
        <Box sx={{ p: 2 }}>
          {/* Add your sources content here */}
          {chunks.length === 0 ? (
            <Typography variant="body2">No sources available.</Typography>
          ) : (
            <>
              {chunks.map((chunk, idx) => (
                <Box
                  key={chunk.id ?? idx}
                  sx={{
                    mb: 3,
                    p: 2,
                    border: '1px solid',
                    borderColor: 'divider',
                    borderRadius: 2,
                    bgcolor: '#f5f5f5', // grey background
                  }}
                >
                  <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 'bold' }}>
                    {chunk.book_name} — Page {chunk.page_number}
                  </Typography>
                  <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
                    {chunk.page_content}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
                    <IconButton
                      color={chunkFeedback[idx] === 'up' ? 'primary' : 'default'}
                      onClick={() =>
                        setChunkFeedback((prev) => ({
                          ...prev,
                          [idx]: prev[idx] === 'up' ? null : 'up',
                        }))
                      }
                    >
                      <ThumbUpAltOutlinedIcon />
                    </IconButton>
                    <IconButton
                      color={chunkFeedback[idx] === 'down' ? 'primary' : 'default'}
                      onClick={() =>
                        setChunkFeedback((prev) => ({
                          ...prev,
                          [idx]: prev[idx] === 'down' ? null : 'down',
                        }))
                      }
                      >
                        <ThumbDownAltOutlinedIcon />
                    </IconButton>
                  </Box>
                </Box>
              ))}
              <Button
                variant="contained"
                sx={{ mt: 2, width: '50%', height: 24, mx: 'auto', display: 'block', minHeight: 0, padding: 0 }}
                
                onClick={handleCloseSourcePanel}
              >
               <Done />
              </Button>
            </>
          )}
        </Box>
      </Drawer>

      {/* Input field and send button */}
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
          disabled={loading}
        />
        <Button
          variant="contained"
          endIcon={<SendIcon />}
          onClick={handleSend}
          sx={{ minWidth: 100 }}
          disabled={loading}
        >
          Send
        </Button>
      </Box>
    </Container>
  );
};

export default ChatPage;
