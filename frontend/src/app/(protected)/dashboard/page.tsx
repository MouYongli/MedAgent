'use client';

import React from 'react';
import { Typography, Grid, Card, CardContent, Box } from '@mui/material';

const DashboardPage: React.FC = () => {
  const stats = [
    { title: 'Total Users', value: 1500 },
    { title: 'Active Sessions', value: 300 },
    { title: 'New Signups', value: 25 },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      <Typography variant="body1" paragraph>
        Here you can see a quick snapshot of system metrics.
      </Typography>

      <Grid container spacing={2}>
        {stats.map((item, index) => (
          <Grid item key={index} xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {item.title}
                </Typography>
                <Typography variant="h4" color="primary">
                  {item.value}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default DashboardPage;
