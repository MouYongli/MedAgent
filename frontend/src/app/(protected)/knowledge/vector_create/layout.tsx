'use client';

import React from 'react';
import { Layout } from 'antd';

const { Content } = Layout;

interface VectorCreateLayoutProps {
  children: React.ReactNode;
}

const VectorCreateLayout: React.FC<VectorCreateLayoutProps> = ({ children }) => {
  return (
    <Content
      style={{
        background: '#fff',
        margin: 0,
      }}
    >
      {children}
    </Content>
  );
};

export default VectorCreateLayout;
