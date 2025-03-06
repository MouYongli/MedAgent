'use client';
import React from 'react';
import { Box } from '@mui/material';
import KnowledgeSidebar from '@/components/common/Sidebar/KnowledgeSidebar';

interface KnowledgeLayoutProps {
  children: React.ReactNode;
}

const KnowledgeLayout: React.FC<KnowledgeLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      {/* 左侧 Sidebar */}
      <Box
        component="aside"
        sx={{
          width: 200,
          flexShrink: 0,
          bgcolor: 'background.paper'
        }}
      >
        <KnowledgeSidebar />
      </Box>

      {/* 右侧内容区域 */}
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

export default KnowledgeLayout;
