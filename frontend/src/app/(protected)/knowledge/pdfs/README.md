# Knowledge Page 知识库页面

## 页面结构

知识库页面采用左右布局设计：
- 左侧：导航侧边栏 (KnowledgeSidebar)
- 右侧：内容显示区域

### 主要组件

1. `layout.tsx`
   - 负责整体页面布局
   - 集成了左侧导航栏和右侧内容区域
   - 使用 Material-UI 的 Box 组件实现弹性布局

2. `page.tsx`
   - 知识库首页内容
   - 显示欢迎信息和基本导航链接
   - 提供到 PDF 文件区域的快捷链接

3. `KnowledgeSidebar.tsx`
   - 位置：`@/components/common/Sidebar/KnowledgeSidebar`
   - 提供三个主要导航分类：
     - Knowledge Base（知识库）
       - PDF Files
       - Vector Databases
     - Search（搜索）
       - Quick Search
       - Advanced Search
     - User Settings（用户设置）
       - My Profile
       - Settings

### 功能特点

1. 响应式布局
   - 侧边栏固定宽度：200px
   - 内容区域自适应宽度

2. 导航功能
   - 可折叠的菜单项
   - 当前选中项高亮显示
   - 支持子菜单展开/收起

3. PDF 文件管理
   - 独立的 PDF 文件页面
   - 通过 API 获取 PDF 文件列表
   - 位于 `/knowledge/pdfs` 路径

## 技术栈

- Material-UI (MUI)
- react-pdf-viewer

## 开发指南

### 添加新的知识库内容

1. 在 `pdfs` 目录下添加新的 PDF 文件
2. 更新后端 API 以支持新添加的文件
3. 文件会自动显示在 PDF 文件列表中

### 扩展侧边栏

在 `KnowledgeSidebar.tsx` 的 `menuItems` 数组中添加新的菜单项：

```typescript
{
  key: 'your-key',
  icon: <YourIcon />,
  label: 'Your Label',
  children: [
    { key: 'sub-item', label: 'Sub Item' },
  ],
}
```

### API 集成

PDF 文件列表通过以下 API 端点获取：
