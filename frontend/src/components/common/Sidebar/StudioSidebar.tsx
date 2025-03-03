'use client';

import React from 'react';
import { Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import { EditOutlined, FolderOpenOutlined, SettingsOutlined } from '@mui/icons-material';

const items = [
  {
    key: 'projects',
    icon: <EditOutlined />,
    label: 'Projects',
  },
  {
    key: 'assets',
    icon: <FolderOpenOutlined />,
    label: 'Assets',
  },
  {
    key: 'settings',
    icon: <SettingsOutlined />,
    label: 'Settings',
  },
];

const StudioSidebar: React.FC = () => {
  return (
    <Menu
      mode="inline"
      defaultSelectedKeys={['projects']}
      style={{ height: '100%', borderRight: 0 }}
    >
      {items.map((item) => (
        <MenuItem key={item.key}>
          <ListItemIcon>{item.icon}</ListItemIcon>
          <ListItemText primary={item.label} />
        </MenuItem>
      ))}
    </Menu>
  );
};

export default StudioSidebar;
