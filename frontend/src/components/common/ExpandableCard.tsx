'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, Button, Typography, Box } from '@mui/material';

interface ExpandableCardProps {
  icon: React.ReactNode;
  title: string;
  text: string;
}

const ExpandableCard: React.FC<ExpandableCardProps> = ({ icon, title, text }) => {
  const [expanded, setExpanded] = useState(false);
  const [needsExpand, setNeedsExpand] = useState(false);
  const contentRef = useRef<HTMLDivElement>(null);

  // 固定展示区域高度（初始折叠状态）
  const COLLAPSED_HEIGHT = 150;

  useEffect(() => {
    if (contentRef.current) {
      // 当内容的实际高度超出折叠高度时，显示"点击详情"
      if (contentRef.current.scrollHeight > COLLAPSED_HEIGHT) {
        setNeedsExpand(true);
      }
    }
  }, []);

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  return (
    <Card
      sx={{
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        textAlign: 'center',
      }}
    >
      <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ mb: 2 }}>{icon}</Box>
        <Typography variant="h5" component="h3" gutterBottom>
          {title}
        </Typography>
        <Box
          ref={contentRef}
          sx={{
            overflow: 'hidden',
            height: expanded ? 'auto' : COLLAPSED_HEIGHT,
            transition: 'height 0.3s',
            mb: 2,
          }}
        >
          <Typography variant="body1" color="text.secondary">
            {text}
          </Typography>
        </Box>
        {needsExpand && (
          <Button
            onClick={toggleExpand}
            color="primary"
            sx={{ mt: 'auto' }}
          >
            {expanded ? '收起' : '点击详情'}
          </Button>
        )}
      </CardContent>
    </Card>
  );
};

export default ExpandableCard;
