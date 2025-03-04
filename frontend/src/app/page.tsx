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

  // 示例长文本，可以根据实际数据调整
  const longText1 = '利用 RAG 框架，实现文献、指南的精准检索，为问答提供有力的知识支持。' +
    ' 这部分内容可能会比较长，如果超出一定高度则会自动折叠，点击详情可展开查看更多详细信息。';
    
  const longText2 = '结合大语言模型，自动生成专业且易懂的回答，助力医疗决策与指导。' +
    ' 此处文本内容同样可能较长，需要根据实际情况进行折叠处理。';
    
  const longText3 = '完整的 AI 工作流，涵盖数据预处理、模型训练、实时推理与反馈，确保结果精准可靠。' +
    ' 额外的说明信息可能会使内容溢出固定区域，用户可点击详情展开查看更多内容。';

  return (
    <Box sx={{ py: 3, bgcolor: 'grey.100' }}>
      {/* 英雄区 */}
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

        {/* 系统介绍 - 三个卡片保持等高 */}
        <Grid container spacing={3} justifyContent="center">
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Rocket sx={{ fontSize: 40, color: 'primary.main' }} />}
              title="高效检索"
              text={longText1}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Search sx={{ fontSize: 40, color: 'success.main' }} />}
              title="智能问答"
              text={longText2}
            />
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <ExpandableCard
              icon={<Science sx={{ fontSize: 40, color: 'warning.main' }} />}
              title="AI 工作流"
              text={longText3}
            />
          </Grid>
        </Grid>

        <Divider sx={{ my: 6 }} />

        {/* 使用案例 */}
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
            系统演示
          </Typography>
          <Typography variant="h6" color="text.secondary" paragraph>
            输入您的医疗问题，我们的系统将结合最新指南和文献，为您提供个性化的解答和推荐。
          </Typography>
          <Link href="/chat" style={{ textDecoration: 'none' }}>
            <Button variant="contained" size="large">
              开始问答
            </Button>
          </Link>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;

