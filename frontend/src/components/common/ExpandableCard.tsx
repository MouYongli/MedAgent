'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Card, Button, Typography } from '@mui/material';

const { Title, Paragraph } = Typography;

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
      // 当内容的实际高度超出折叠高度时，显示“点击详情”
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
      variant="outlined"
      style={{
        textAlign: 'center',
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
      }}
    >
      <div>{icon}</div>
      <Title level={4} style={{ marginTop: '16px' }}>
        {title}
      </Title>
      <div
        ref={contentRef}
        style={{
          overflow: 'hidden',
          height: expanded ? 'auto' : COLLAPSED_HEIGHT,
          transition: 'height 0.3s',
        }}
      >
        <Paragraph>{text}</Paragraph>
      </div>
      {needsExpand && (
        <Button variant="text" onClick={toggleExpand}>
          {expanded ? '收起' : '点击详情'}
        </Button>
      )}
    </Card>
  );
};

export default ExpandableCard;
