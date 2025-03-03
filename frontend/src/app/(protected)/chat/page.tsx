'use client';

import React, { useState } from 'react';
import { List, TextField, Button, Typography, Divider } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const { Text } = Typography;

interface Message {
  id: number;
  sender: string;
  content: string;
  isMine: boolean;
}

const ChatPage: React.FC = () => {
  // 初始聊天记录（示例）
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, sender: 'Alice', content: 'Hello there!', isMine: false },
    { id: 2, sender: 'You', content: 'Hi, Alice!', isMine: true },
  ]);

  // 文本框内容
  const [inputValue, setInputValue] = useState('');

  // 发送消息
  const handleSend = () => {
    if (!inputValue.trim()) return;
    setMessages((prev) => [
      ...prev,
      {
        id: prev.length + 1,
        sender: 'You',
        content: inputValue,
        isMine: true,
      },
    ]);
    setInputValue('');
  };

  return (
    <div style={styles.container}>
      <Divider orientation="left" style={{ fontSize: '1.25rem' }}>
        Chat with Alice
      </Divider>

      {/* 消息列表 */}
      <List
        dataSource={messages}
        renderItem={(item) => {
          const bubbleStyle = item.isMine
            ? { ...styles.bubble, ...styles.bubbleMine }
            : { ...styles.bubble, ...styles.bubbleOther };
          const itemStyle = item.isMine
            ? { justifyContent: 'flex-end' }
            : { justifyContent: 'flex-start' };

          return (
            <List.Item style={{ display: 'flex', ...itemStyle }}>
              <div style={bubbleStyle}>
                <Text style={{ color: item.isMine ? '#fff' : '#000' }}>
                  {item.content}
                </Text>
              </div>
            </List.Item>
          );
        }}
      />

      {/* 输入框和发送按钮 */}
      <div style={styles.inputArea}>
        <TextField
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSend();
            }
          }}
          placeholder="Enter the message..."
          style={{ marginRight: 8 }}
        />
        <Button
          variant="contained"
          color="primary"
          endIcon={<SendIcon />}
          onClick={handleSend}
        >
          Send
        </Button>
      </div>
    </div>
  );
};

// 简易内联样式
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: 800,
    margin: '0 auto',
    padding: 24,
  },
  bubble: {
    padding: '8px 12px',
    borderRadius: 16,
    maxWidth: '60%',
    wordWrap: 'break-word',
  },
  bubbleMine: {
    backgroundColor: '#1976d2',
    color: '#fff',
  },
  bubbleOther: {
    backgroundColor: '#f0f0f0',
    color: '#000',
  },
  inputArea: {
    display: 'flex',
    marginTop: 16,
  },
};

export default ChatPage;
