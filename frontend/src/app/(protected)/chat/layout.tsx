'use client';
import React from 'react';
import { Box, Grid } from '@mui/material';
import ChatSidebar from '@/components/common/Sidebar/ChatSidebar';

interface ChatLayoutProps {
  children: React.ReactNode;
}

const ChatLayout: React.FC<ChatLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex' }}>
      {/* 左侧 Sider */}
      <Box sx={{ width: 200, background: '#fff' }}>
        <ChatSidebar />
      </Box>

      {/* 右侧内容区域 */}
      <Box sx={{ flex: 1, padding: '24px' }}>
        <Box
          sx={{
            background: '#fff',
            padding: '24px',
            margin: 0,
            minHeight: 280,
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default ChatLayout;
