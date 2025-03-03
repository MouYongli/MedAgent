'use client';

import React from 'react';
import { Typography, Divider } from 'antd';

const { Title, Paragraph } = Typography;

const VectorCreatePage: React.FC = () => {
  return (
    <div>
      <Title level={2}>Create new vector database</Title>
      <Paragraph>
        Create a new vector database by uploading PDFs, chunking them, and ultimately storing them in a vector database.
      </Paragraph>
      <Divider />
      <Paragraph>
        <strong>TODO:</strong> Three sections
      </Paragraph>
    </div>
  );
};

export default VectorCreatePage;
