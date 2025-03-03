'use client';

import React from 'react';
import { Typography, Divider } from '@mui/material';

const { Title, Paragraph } = Typography;

const StudioPage: React.FC = () => {
  return (
    <div>
      <Title level={2}>Studio Overview</Title>
      <Paragraph>
        This is the main page for the Studio module. You can manage projects, assets, and settings here.
      </Paragraph>
      <Divider />
      <Paragraph>
        <strong>Projects:</strong> Create and edit your ongoing projects.
      </Paragraph>
      <Paragraph>
        <strong>Assets:</strong> Upload and organize media or other resources.
      </Paragraph>
      <Paragraph>
        <strong>Settings:</strong> Configure the studio environment and user preferences.
      </Paragraph>
    </div>
  );
};

export default StudioPage;
