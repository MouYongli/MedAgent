'use client';

import React from 'react';
import { Box } from '@mui/material';
import StudioSidebar from '@/components/common/Sidebar/StudioSidebar';

interface StudioLayoutProps {
  children: React.ReactNode;
}

const StudioLayout: React.FC<StudioLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Box
        component="aside"
        sx={{
          width: 200,
          flexShrink: 0,
          bgcolor: 'background.paper'
        }}
      >
        <StudioSidebar />
      </Box>
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

export default StudioLayout;
