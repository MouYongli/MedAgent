'use client';

import React from 'react';
import { Typography, Divider } from 'antd';

const { Title, Paragraph } = Typography;

const StudioPage: React.FC = () => {
  return (
    <div>
      <Title level={2}>Knowledge overview</Title>
      <Paragraph>
        This is the main page for the Knowledge module. Meaning, new knowledge bases of pre-defined types can be created and alternated.
      </Paragraph>
      <Divider />
      <Paragraph>
        <strong>TODO:</strong> Include overview and creation of vector database.
      </Paragraph>
    </div>
  );
};

export default StudioPage;
