'use client';

import React from 'react';
import { Typography, Divider, Box, Container, Link } from '@mui/material';

const KnowledgePage: React.FC = () => {
  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        Knowledge Base
      </Typography>
      <Divider sx={{ mb: 3 }} />

      <Box sx={{ mt: 2 }}>
        <Typography variant="body1">
          Welcome to the Knowledge Base. Here you can find various articles and tutorials to help you.
        </Typography>
        <Link href="/knowledge/pdfs" sx={{ mt: 2, display: 'block' }}>
          PDF Files
        </Link>
        <Link href="/knowledge/kgindexer" sx={{ mt: 2, display: 'block' }}>
          Knowledge Graph
        </Link>
      </Box>
    </Container>
  );
};

export default KnowledgePage;
