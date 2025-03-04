'use client';

import React from 'react';
import { Typography, Divider, Box } from '@mui/material';

const StudioPage: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Studio Overview
      </Typography>
      <Typography variant="body1" paragraph>
        This is the main page for the Studio module. You can manage projects, assets, and settings here.
      </Typography>
      <Divider sx={{ my: 3 }} />
      <Typography variant="body1" paragraph>
        <strong>Projects:</strong> Create and edit your ongoing projects.
      </Typography>
      <Typography variant="body1" paragraph>
        <strong>Assets:</strong> Upload and organize media or other resources.
      </Typography>
      <Typography variant="body1" paragraph>
        <strong>Settings:</strong> Configure the studio environment and user preferences.
      </Typography>
    </Box>
  );
};

export default StudioPage;
