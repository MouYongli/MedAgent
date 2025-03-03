// // app/page.tsx
'use client';

import React from 'react';
import { Typography, Grid, Button, Container, Box, Divider } from '@mui/material';
import { Rocket, Search, Science } from '@mui/icons-material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import ExpandableCard from '@/components/common/ExpandableCard';

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  // Example long text, can be adjusted based on actual data
  const longText1 =
    'Using the RAG framework, precisely retrieve literature and guidelines to provide strong knowledge support for Q&A.' +
    ' This section may be relatively long. If it exceeds a certain height, it will automatically collapse. Click "More Details" to expand and view additional information.';

  const longText2 =
    'Combining large language models to automatically generate professional and easy-to-understand answers, assisting medical decision-making and guidance.' +
    ' This text may also be lengthy and needs to be collapsed based on actual conditions.';

  const longText3 =
    'A complete AI workflow covering data preprocessing, model training, real-time inference, and feedback, ensuring accurate and reliable results.' +
    ' Additional explanatory information may overflow the fixed area, and users can click "More Details" to expand and see more content.';

  return (
    <Box sx={{ py: 3, bgcolor: 'grey.100' }}>
      {/* Hero section */}
      <Container>
        <Box
          sx={{
            textAlign: 'center',
            mb: 6,
            py: 5,
            px: 2,
            bgcolor: 'background.paper',
            borderRadius: 2,
          }}
        >
          <Typography variant="h2" component="h1" gutterBottom>
            {t('home.title')}
          </Typography>
          <Typography variant="h5" color="text.secondary" paragraph>
            {t('home.subtitle')}
          </Typography>
          <Link href="/chat" style={{ textDecoration: 'none' }}>
            <Button variant="contained" size="large">
              {t('home.try_now')}
            </Button>
          </Link>
        </Box>

        <Divider sx={{ my: 6 }} />

        {/* System Introduction - Three equally high cards */}
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Rocket sx={{ fontSize: 40, color: 'primary.main' }} />}
              title="Efficient Retrieval"
              text={longText1}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Search sx={{ fontSize: 40, color: 'success.main' }} />}
              title="Intelligent Q&A"
              text={longText2}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Science sx={{ fontSize: 40, color: 'warning.main' }} />}
              title="AI Workflow"
              text={longText3}
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 6 }} />

        {/* Use Case Demonstration */}
        <Box
          sx={{
            bgcolor: 'background.paper',
            py: 5,
            px: 2,
            borderRadius: 2,
            textAlign: 'center',
          }}
        >
          <Typography variant="h4" component="h3" gutterBottom>
            System Demonstration
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph>
            Enter your medical question, and our system will combine the latest guidelines and literature to provide you with personalized answers and recommendations.
          </Typography>
          <Link href="/chat" style={{ textDecoration: 'none' }}>
            <Button variant="contained" size="large">
              Start Q&A
            </Button>
          </Link>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;

