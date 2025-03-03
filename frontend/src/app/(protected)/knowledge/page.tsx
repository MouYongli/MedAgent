'use client';

import React from 'react';
import { Typography, Divider, Box, Container, Link } from '@mui/material';

/* maybe use const { Title, Paragraph } = Typography; */

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
          <strong>TODO:</strong> Include overview and creation of vector database.
        </Typography>
        <Link href="/knowledge/pdfs" sx={{ mt: 2, display: 'block' }}>
          PDF Files
        </Link>
      </Box>
    </Container>
  );
};

export default KnowledgePage;
