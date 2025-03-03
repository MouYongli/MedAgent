'use client';

import React from 'react';
import { Menu, MenuItem, ListItemIcon, ListItemText } from '@mui/material';
import { DashboardOutlined, BarChartOutlined, FileOutlined } from '@mui/icons-material';

const items = [
  {
    key: 'overview',
    icon: <DashboardOutlined />,
    label: 'Overview',
  },
  {
    key: 'analytics',
    icon: <BarChartOutlined />,
    label: 'Analytics',
  },
  {
    key: 'reports',
    icon: <FileOutlined />,
    label: 'Reports',
  },
];

const DashboardSidebar: React.FC = () => {
  return (
    <Menu
      mode="inline"
      defaultSelectedKeys={['overview']}
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

export default DashboardSidebar;
