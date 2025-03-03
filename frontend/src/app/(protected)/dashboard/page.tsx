'use client';

import React from 'react';
import { Typography, Grid, Card } from '@mui/material';

const { Title, Paragraph } = Typography;

const DashboardPage: React.FC = () => {
  const stats = [
    { title: 'Total Users', value: 1500 },
    { title: 'Active Sessions', value: 300 },
    { title: 'New Signups', value: 25 },
  ];

  return (
    <div>
      <Title level={2}>Dashboard Overview</Title>
      <Paragraph>Here you can see a quick snapshot of system metrics.</Paragraph>

      <Grid container spacing={2}>
        {stats.map((item, index) => (
          <Grid item key={index} xs={12} sm={6} md={4}>
            <Card style={{ marginBottom: '16px' }}>
              <Title level={4}>{item.title}</Title>
              <Paragraph style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{item.value}</Paragraph>
            </Card>
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default DashboardPage;
