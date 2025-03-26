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
   - 提供到 PDF 文件列表和pdf 展示

3. `KnowledgeSidebar.tsx`
   - 位置：`@/components/common/Sidebar/KnowledgeSidebar`
   - 提供三个主要导航分类：
     - Knowledge Base（知识库）
       - PDF Files
       - Vector Databases
     - Search（搜索）
       - Quick Search
       - Advanced Search

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

## 技术栈

- Material-UI (MUI)
- react-pdf-viewer

## API 集成

下面的表格展示了如何使用 RESTful API 来获取 PDF 文件列表和访问单个 PDF 文件。请确保 .env 文件中配置了后端数据库地址和端口。

| API Endpoint                     | HTTP Method | Description                                |
| -------------------------------- | ----------- | ------------------------------------------ |
| `http://localhost:8000/`         | GET         | 获取 PDF 文件列表                           |
| `http://localhost:8000/{file}.pdf` | GET         | 访问特定 PDF 文件（例如: `xxxx.pdf`）       |



## 后续开发建议
添加高亮持久化功能：

创建后端 API 存储每个 PDF 的高亮信息
编写 saveHighlightToServer 和 fetchHighlightsForPdf 函数
改进用户体验：

添加删除高亮的功能
考虑添加高亮颜色选择功能
可以添加高亮列表，方便用户查看所有高亮内容
性能优化：

对大型 PDF 文件，考虑分页加载高亮信息