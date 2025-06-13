'use client';

import React, { useEffect, useState } from 'react';
import { Container, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import axios from 'axios';

const KnowledgeGraphPage: React.FC = () => {
  const [KnowledgeGraphPage, setKnowledgeGraphPage] = useState<string[]>([]);

  useEffect(() => {
    const fetchKGIndexer = async () => {
      try {
        const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}:${process.env.NEXT_PUBLIC_BACKEND_PORT}/api/knowledge/pdf`);
        setKnowledgeGraphPage(response.data);
      } catch (error) {
        console.error('Error fetching PDF files:', error);
      }
    };

    fetchKGIndexer();
  }, []);

  return (
    <Container maxWidth="md" sx={{ py: 3 }}>
      <Typography variant="h5" sx={{ mb: 2 }}>
        PDF Files
      </Typography>
      <Divider sx={{ mb: 3 }} />
      <List>
        {KnowledgeGraphPage.map((file, index) => (
          <ListItem key={index}>
            <ListItemText primary={file} />
          </ListItem>
        ))}
      </List>
    </Container>
  );
};

export default KnowledgeGraphPage;
