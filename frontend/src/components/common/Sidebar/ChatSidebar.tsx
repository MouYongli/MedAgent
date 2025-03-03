'use client';
import React from 'react';
import { Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import { MessageOutlined, SearchOutlined, UserOutlined, NotificationOutlined } from '@mui/icons-material';

const items = [
  {
    key: 'chats',
    icon: <MessageOutlined />,
    label: 'My Chats',
    children: [
      { key: 'current', label: 'Current Chat' },
      { key: 'history', label: 'Chat History' },
    ],
  },
  {
    key: 'search',
    icon: <SearchOutlined />,
    label: 'Guidelines',
    children: [
      { key: 'quick-search', label: 'Quick Search' },
      { key: 'favorites', label: 'Available Guidelines' },
    ],
  },
  {
    key: 'center',
    icon: <UserOutlined />,
    label: 'User Settings',
    children: [
      { key: 'profile', label: 'My Profile' },
      { key: 'settings', label: 'Settings' },
    ],
  },
];

const ChatSidebar: React.FC = () => {
  return (
    <Menu
      mode="inline"
      defaultSelectedKeys={['current']}
      defaultOpenKeys={['sub1']}
      style={{ height: '100%', borderRight: 0 }}
    >
      {items.map((item) => (
        <MenuItem key={item.key}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.label} />
          {item.children && (
            <Menu>
              {item.children.map((child) => (
                <MenuItem key={child.key}>
                  <ListItemText primary={child.label} />
                </MenuItem>
              ))}
            </Menu>
          )}
        </MenuItem>
      ))}
    </Menu>
  );
};

export default ChatSidebar;
