'use client';

import React from 'react';
import {List, ListItem, ListItemButton, ListItemIcon, ListItemText} from '@mui/material';
import { Dashboard, BarChart, Description } from '@mui/icons-material';
import { useRouter } from 'next/navigation';

const items = [
  {
    key: 'overview',
    icon: <Dashboard />,
    label: 'Overview',
  },
  {
    key: 'analytics',
    icon: <BarChart />,
    label: 'Analytics',
  },
  {
    key: 'reports',
    icon: <Description />,
    label: 'Reports',
  },
];

const DashboardSidebar: React.FC = () => {
  const router = useRouter();
  const [selectedKey, setSelectedKey] = React.useState('overview');

  const handleItemClick = (key: string) => {
    setSelectedKey(key);
    router.push(`/dashboard/${key}`);
  };

  return (
    <List component="nav" sx={{ height: '100%', borderRight: 1, borderColor: 'divider' }}>
      {items.map((item) => (
        <ListItem key={item.key} disablePadding>
          <ListItemButton
            selected={selectedKey === item.key}
            onClick={() => handleItemClick(item.key)}
            sx={{
              '&.Mui-selected': {
                backgroundColor: 'action.selected',
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
};

export default DashboardSidebar;
