'use client';

import React from 'react';
import { Typography, Grid, Divider, Button } from '@mui/material';
import { RocketLaunchOutlined, SearchOutlined, ScienceOutlined } from '@mui/icons-material';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import ExpandableCard from '@/components/common/ExpandableCard';

const { Title, Paragraph } = Typography;

const HomePage: React.FC = () => {
  const { t } = useTranslation();

  // 示例长文本，可以根据实际数据调整
  const longText1 = '利用 RAG 框架，实现文献、指南的精准检索，为问答提供有力的知识支持。' +
    ' 这部分内容可能会比较长，如果超出一定高度则会自动折叠，点击详情可展开查看更多详细信息。';
    
  const longText2 = '结合大语言模型，自动生成专业且易懂的回答，助力医疗决策与指导。' +
    ' 此处文本内容同样可能较长，需要根据实际情况进行折叠处理。';
    
  const longText3 = '完整的 AI 工作流，涵盖数据预处理、模型训练、实时推理与反馈，确保结果精准可靠。' +
    ' 额外的说明信息可能会使内容溢出固定区域，用户可点击详情展开查看更多内容。';

  return (
    <div style={{ padding: '24px', background: '#f0f2f5' }}>
      {/* 英雄区 */}
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
        <Button variant="contained" color="primary" size="large">
          <Link href="/chat">{t('home.try_now')}</Link>
        </Button>
      </div>

      <Divider />

      {/* 系统介绍 - 三个卡片保持等高 */}
      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12} sm={6} md={4}>
          <ExpandableCard
            icon={<RocketLaunchOutlined style={{ fontSize: '2.5rem', color: '#1890ff' }} />}
            title="高效检索"
            text={longText1}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <ExpandableCard
            icon={<SearchOutlined style={{ fontSize: '2.5rem', color: '#52c41a' }} />}
            title="智能问答"
            text={longText2}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <ExpandableCard
            icon={<ScienceOutlined style={{ fontSize: '2.5rem', color: '#faad14' }} />}
            title="AI 工作流"
            text={longText3}
          />
        </Grid>
      </Grid>

      <Divider style={{ margin: '48px 0' }} />

      {/* 使用案例 */}
      <div
        style={{
          background: '#fff',
          padding: '40px 20px',
          borderRadius: 8,
          textAlign: 'center',
        }}
      >
        <Title level={3}>系统演示</Title>
        <Paragraph style={{ fontSize: '1.1rem' }}>
          输入您的医疗问题，我们的系统将结合最新指南和文献，为您提供个性化的解答和推荐。
        </Paragraph>
        <Button variant="contained" color="primary" size="large">
          <Link href="/chat">开始问答</Link>
        </Button>
      </div>
    </div>
  );
};

export default HomePage;
