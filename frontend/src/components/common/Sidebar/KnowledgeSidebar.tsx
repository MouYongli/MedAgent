'use client';

import React from 'react';
import { Menu } from 'antd';
import type { MenuProps } from 'antd';
import { EditOutlined } from '@ant-design/icons';

const items: MenuProps['items'] = [
  {
    key: 'todo',
    icon: <EditOutlined />,
    label: 'TODO',
  },
];

const StudioSidebar: React.FC = () => {
  return (
    <Menu
      mode="inline"
      defaultSelectedKeys={['todo']}
      style={{ height: '100%', borderRight: 0 }}
      items={items}
    />
  );
};

export default StudioSidebar;
