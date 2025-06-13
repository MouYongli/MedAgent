'use client';
import React from 'react';
import {
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Collapse,
  Box
} from '@mui/material';
import {
  MenuBook as KnowledgeIcon,
  Search as SearchIcon,
  Person as UserIcon,
  ExpandLess,
  ExpandMore
} from '@mui/icons-material';

const menuItems = [
  {
    key: 'knowledge',
    icon: <KnowledgeIcon />,
    label: 'Knowledge Base',
    children: [
      { key: 'pdf', label: 'PDF Files' },
      { key: 'vdb', label: 'Vector Databases' },
      { key: 'kg', label: 'Knowledge Graph' },
    ],
  },
  {
    key: 'search',
    icon: <SearchIcon />,
    label: 'Search',
    children: [
      { key: 'quick-search', label: 'Quick Search' },
      { key: 'advanced-search', label: 'Advanced Search' },
    ],
  },
  {
    key: 'user',
    icon: <UserIcon />,
    label: 'User Settings',
    children: [
      { key: 'profile', label: 'My Profile' },
      { key: 'settings', label: 'Settings' },
    ],
  },
];

const KnowledgeSidebar: React.FC = () => {
  const [openItems, setOpenItems] = React.useState<string[]>(['knowledge']);
  const [selectedItem, setSelectedItem] = React.useState('articles');

  const handleClick = (key: string) => {
    setOpenItems(prev =>
      prev.includes(key) ? prev.filter(item => item !== key) : [...prev, key]
    );
  };

  const handleItemClick = (key: string) => {
    setSelectedItem(key);
  };

  return (
    <Box sx={{ width: '100%', borderRight: 1, borderColor: 'divider' }}>
      <List component="nav">
        {menuItems.map((item) => (
          <React.Fragment key={item.key}>
            <ListItemButton onClick={() => handleClick(item.key)}>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
              {openItems.includes(item.key) ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Collapse in={openItems.includes(item.key)} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {item.children?.map((child) => (
                  <ListItemButton
                    key={child.key}
                    selected={selectedItem === child.key}
                    onClick={() => handleItemClick(child.key)}
                    sx={{ pl: 4 }}
                  >
                    <ListItemText primary={child.label} />
                  </ListItemButton>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default KnowledgeSidebar;
