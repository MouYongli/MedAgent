'use client';

import React from 'react';
import {
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box
} from '@mui/material';
import {
  Edit as EditIcon,
  Folder as FolderIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

const items = [
  {
    key: 'projects',
    icon: <EditIcon />,
    label: 'Projects',
  },
  {
    key: 'assets',
    icon: <FolderIcon />,
    label: 'Assets',
  },
  {
    key: 'settings',
    icon: <SettingsIcon />,
    label: 'Settings',
  },
];

const StudioSidebar: React.FC = () => {
  const [selectedItem, setSelectedItem] = React.useState('projects');

  const handleItemClick = (key: string) => {
    setSelectedItem(key);
  };

  return (
    <Box sx={{ width: '100%', borderRight: 1, borderColor: 'divider' }}>
      <List component="nav">
        {items.map((item) => (
          <ListItemButton
            key={item.key}
            selected={selectedItem === item.key}
            onClick={() => handleItemClick(item.key)}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Box>
  );
};

export default StudioSidebar;
