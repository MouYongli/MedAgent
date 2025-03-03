import React from 'react';
import { Box, Typography } from '@mui/material';

const AppFooter: React.FC = () => {
  return (
    <Box sx={{ textAlign: 'center', padding: '20px', backgroundColor: '#f0f0f0' }}>
      <Typography variant="body2" color="textSecondary">
        MedAgent ©2025 Created by RWTH (DBIS)
      </Typography>
    </Box>
  );
};

export default AppFooter;
