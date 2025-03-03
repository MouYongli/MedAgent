'use client';

import React from 'react';
import { Menu } from 'antd';
import type { MenuProps } from 'antd';
import { EditOutlined, PlusOutlined } from '@ant-design/icons';
import Link from "next/link";

const items: MenuProps['items'] = [
  {
    key: 'todo',
    icon: <EditOutlined />,
    label: <Link href="/knowledge/">{'TODO'}</Link>,
  },
  {
    key: 'create vector',
    icon: <PlusOutlined />,
    label: <Link href="/knowledge/vector_create">{'Create new vector DB'}</Link>
  }
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
