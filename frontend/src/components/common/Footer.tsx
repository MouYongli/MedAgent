// components/common/Footer.tsx
import React from 'react';
import { Box, Container, Typography } from '@mui/material';

const AppFooter: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[100]
      }}
    >
      <Container maxWidth="sm">
        <Typography variant="body2" color="text.secondary" align="center">
          MedAgent ©2025 Created by RWTH (DBIS)
        </Typography>
      </Container>
    </Box>
  );
};

export default AppFooter;
