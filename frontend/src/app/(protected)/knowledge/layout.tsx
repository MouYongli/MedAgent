'use client';

import React from 'react';
import { Layout } from 'antd';
import KnowledgeSidebar from "@/components/common/Sidebar/KnowledgeSidebar";

const { Sider, Content } = Layout;

interface StudioLayoutProps {
  children: React.ReactNode;
}

const KnowledgeLayout: React.FC<StudioLayoutProps> = ({ children }) => {
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={200} style={{ background: '#fff' }}>
        <KnowledgeSidebar />
      </Sider>
      <Layout style={{ padding: '24px' }}>
        <Content
          style={{
            background: '#fff',
            padding: '24px',
            margin: 0,
            minHeight: 280,
          }}
        >
          {children}
        </Content>
      </Layout>
    </Layout>
  );
};

export default KnowledgeLayout;
