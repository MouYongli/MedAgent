'use client';

import React from 'react';
import { Box } from '@mui/material';
import DashboardSidebar from '@/components/common/Sidebar/DashboardSidebar';
import withRole from '@/auth/withRole';

interface DashboardLayoutProps {
  children: React.ReactNode;
}

const DashboardLayout: React.FC<DashboardLayoutProps> = ({ children }) => {
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
        <DashboardSidebar />
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

export default withRole(DashboardLayout, ['admin']);
