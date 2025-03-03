// // app/page.tsx
'use client';

import React from 'react';
import { Typography, Row, Col, Divider, Button } from 'antd';
import { RocketOutlined, SearchOutlined, ExperimentOutlined } from '@ant-design/icons';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import ExpandableCard from '@/components/common/ExpandableCard';

const { Title, Paragraph } = Typography;

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
    <div style={{ padding: '24px', background: '#f0f2f5' }}>
      {/* Hero Section */}
      <div
        style={{
          textAlign: 'center',
          marginBottom: '48px',
          padding: '40px 20px',
          background: '#fff',
          borderRadius: 8,
        }}
      >
        <Title>{t('home.title')}</Title>
        <Paragraph style={{ fontSize: '1.1rem' }}>
          {t('home.subtitle')}
        </Paragraph>
        <Button type="primary" size="large">
          <Link href="/chat">{t('home.try_now')}</Link>
        </Button>
      </div>

      <Divider />

      {/* System Introduction - Three equally high cards */}
      <Row gutter={[24, 24]} justify="center">
        <Col xs={24} sm={12} md={8}>
          <ExpandableCard
            icon={<RocketOutlined style={{ fontSize: '2.5rem', color: '#1890ff' }} />}
            title="Efficient Retrieval"
            text={longText1}
          />
        </Col>
        <Col xs={24} sm={12} md={8}>
          <ExpandableCard
            icon={<SearchOutlined style={{ fontSize: '2.5rem', color: '#52c41a' }} />}
            title="Intelligent Q&A"
            text={longText2}
          />
        </Col>
        <Col xs={24} sm={12} md={8}>
          <ExpandableCard
            icon={<ExperimentOutlined style={{ fontSize: '2.5rem', color: '#faad14' }} />}
            title="AI Workflow"
            text={longText3}
          />
        </Col>
      </Row>

      <Divider style={{ margin: '48px 0' }} />

      {/* Use Case Demonstration */}
      <div
        style={{
          background: '#fff',
          padding: '40px 20px',
          borderRadius: 8,
          textAlign: 'center',
        }}
      >
        <Title level={3}>System Demonstration</Title>
        <Paragraph style={{ fontSize: '1.1rem' }}>
          Enter your medical question, and our system will combine the latest guidelines and literature to provide you with personalized answers and recommendations.
        </Paragraph>
        <Button type="primary" size="large">
          <Link href="/chat">Start Q&A</Link>
        </Button>
      </div>
    </div>
  );
};

export default HomePage;
