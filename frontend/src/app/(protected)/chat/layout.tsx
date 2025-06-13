// src/app/(protected)/chat/layout.tsx
'use client';
import React from 'react';
import { Box } from '@mui/material';
import ChatSidebar from '@/components/common/Sidebar/ChatSidebar';

interface ChatLayoutProps {
  children: React.ReactNode;
}

const ChatLayout: React.FC<ChatLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* Left Sidebar */}
      <Box
        component="aside"
        sx={{
          width: 200,
          flexShrink: 0,
          bgcolor: 'background.paper'
        }}
      >
        <ChatSidebar />
      </Box>

      {/* Right content area */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          bgcolor: 'background.paper',
          borderRadius: 1,
          boxShadow: 1
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default ChatLayout;

