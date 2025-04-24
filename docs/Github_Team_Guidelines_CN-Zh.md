# GitHub团队指南

## Issue使用规范指南

### 1. 明确命名规范

- **清晰简洁**：每个 Issue 的标题应简洁明了，概述问题或任务的核心内容。
    - 例如：
        - **Bug**: Fix bug in login page
        - **Feature**: Implement new feature for data export
- **使用前缀**：根据 Issue 类型或优先级，使用前缀标明 Issue 的性质：
    - **Bug**: 修复 bug
    - **Feature**: 新功能开发
    - **Improvement**: 优化或提升现有功能
    - **Documentation**: 文档更新
    - **Chore**: 维护任务

### 2. 描述规范

- **清晰的描述**：确保描述清晰、详细，明确指出问题的背景、影响范围、出现的具体步骤或预期效果。
- **复现步骤（如果是 Bug）**：如果是 Bug，添加复现步骤，说明 bug 如何触发，帮助开发者更快定位问题。
  ```text
  Steps to reproduce:
  1. Go to the login page.
  2. Enter valid username and password.
  3. Click "Login".
  4. Error: "Invalid credentials" is shown.
  ```
- **预期行为 vs 实际行为**：说明期望的行为和实际发生的情况。
- **截图/视频**：如果可能，提供截图、录屏或日志文件，帮助快速理解问题。

### 3. 任务分配和负责人

- **指定负责人**：在创建 Issue 后，分配合适的团队成员作为负责人，明确谁负责此任务。
- **使用 Assignee**：通过 GitHub 的 "Assignee" 功能，指定一个或多个开发者来负责该 Issue。

### 4. 标签（Labels）

**使用标签分类**：使用 GitHub 提供的标签（如 bug, enhancement, help wanted, good first issue 等）帮助团队快速识别问题类型。
**优先级标签**：设置优先级标签（如 high priority, low priority）帮助团队按优先级处理任务。

### 5. 模板化 (Issue Templates)

创建 Issue 模板：使用 GitHub 的 Issue 模板功能来确保每次创建 Issue 时都有统一的结构。例如，对于 Bug
问题，可以定义一个模板，其中包括复现步骤、预期行为等字段。
定制模板：根据项目的需求创建不同类型的模板，如 Bug, Feature, Documentation, Task 等。

## 6. 设置适当的里程碑

里程碑 (Milestones)：将 Issues 分配到特定的里程碑（例如版本发布或迭代）来跟踪进度。确保每个重要的版本或任务周期都有一个清晰的里程碑，并将相关的
Issue 关联到该里程碑。

### 7. 使用“Draft”功能

草稿功能：对于不完全准备好的 Issue，可以先将其标记为草稿，避免其他成员被误导。草稿状态可以帮助整理问题或需求，直到准备好更多信息后再发布。

### 8. 关联和链接其他 Issue

**跨 Issue 关联**：如果某个任务与其他任务相关，使用 # 来引用其它 Issue。

```text
This task depends on Issue #15 being completed.
```

**文档和 PR 关联**：在提交 PR 时，可以在 PR 描述中链接到相应的 Issue，帮助团队成员了解 PR 修复了哪些问题。

```text
Fixes #34
```

### 9. 关闭问题

适时关闭 Issue：当问题被解决或者任务完成时，及时关闭对应的 Issue，避免堆积未完成的任务。
添加备注：关闭时可以在评论中标明“已解决”或“已合并”，以便后续查看。

### 10. 定期整理与复盘

定期回顾：团队应定期回顾和整理 GitHub Issues，确保所有问题都得到跟踪并适时完成。
复盘未完成的任务：对于长时间未完成的任务，团队可以进行复盘，讨论是否需要调整优先级或分配新的负责人。

### 11. 评论和沟通

清晰的评论：团队成员在讨论时应保持评论简洁明了，避免过多的无关信息。
定期更新：确保在 Issue 中有定期的更新，尤其是当任务有变更时。比如，任务完成、问题定位、需求变化等。

## 及分支管理指南

### 1. 为每个 Issue 创建分支

在开发过程中，通常会为每个 Issue 创建一个对应的分支，确保每个任务或 bug 修复都是在独立的环境中进行的，而不干扰其他任务的进展。分支命名通常与
Issue 号或描述相关。

示例：

```bash
git checkout -b feature/issue-42
```

### 2. 使用分支命名规范

为了保持项目结构的整洁和一致，建议团队使用统一的分支命名规范：

- feature/"issue-number"：用于开发新功能，例如 feature/issue-42。
- bugfix/"issue-number"：用于修复 bug，例如 bugfix/issue-42。
- hotfix/"issue-number"：用于紧急修复，常用于生产环境的问题，例如 hotfix/issue-42。

### 3. 通过 Pull Request (PR) 关闭 Issue

当在分支上完成开发工作并准备合并回主分支时，可以通过 PR 将分支合并到主分支（如 main 或 master）。

在 PR 描述中引用对应的 Issue，合并 PR 后，GitHub 会自动关闭该 Issue。

```text
Fixes #42
```

### 4. 定期同步分支

在多人协作开发时，为了避免与主分支产生冲突，定期同步分支非常重要。

示例：

```bash
git checkout main
git pull origin main
git checkout feature/issue-42
git merge main
```

### 5. 安全性和敏感信息

避免暴露敏感信息：在 GitHub Issues 中，不应包含密码、API 密钥等敏感信息。可以使用 GitHub Secrets 或其他安全机制来处理这些数据。将配置的变量模版放在
**config.yaml.example**，本地配置**config.yaml**，并将这个文件写到**gitignore**文件中。
