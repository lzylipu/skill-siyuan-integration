---
name: siyuan-integration
description: "SiYuan Note integration - persist data to SiYuan Notes via API"
version: 1.0.0
author: lzylipu
license: MIT
platforms: [linux]
prerequisites:
  env_vars: [SIYUAN_ENDPOINT, SIYUAN_TOKEN, SIYUAN_NOTEBOOK_ID]
  services:
    - name: SiYuan Notes
      url: https://b3log.org/siyuan/
      description: "Self-hosted SiYuan Notes instance"
metadata:
  hermes:
    tags: [siyuan, notes, integration, persist, archive, 思源, 笔记, 归档]
    related_skills: [session-archiver, obsidian]
    homepage: https://github.com/lzylipu/skill-siyuan-integration
    category: personal
    skill_type: automation
---

# SiYuan Integration - 思源笔记集成

思源笔记API客户端，用于将课程任务数据持久化到思源笔记系统。

## 功能特性

- **文档创建**: 在思源笔记中创建新文档
- **内容插入**: 向现有文档插入内容
- **资产管理**: 上传和管理文件资产
- **会话归档**: 自动归档当前会话内容
- **课程任务集成**: 专门针对课程任务的数据导入

## 配置

### 1. 环境变量配置

```bash
# 思源笔记API端点
export SIYUAN_ENDPOINT="http://YOUR_SERVER_IP:7000"

# API Token
export SIYUAN_TOKEN="YOUR_SIYUAN_TOKEN"

# 笔记本ID
export SIYUAN_NOTEBOOK="YOUR_NOTEBOOK_ID"

# 目标路径
export SIYUAN_TARGET_PATH="/课程任务"
```

### 2. 配置文件配置

或使用 `siyuan-config.json.example` 配置文件：

```json
{
  "endpoint": "http://YOUR_SERVER_IP:7000",
  "token": "YOUR_SIYUAN_TOKEN",
  "notebook_id": "YOUR_NOTEBOOK_ID",
  "target_path": "/课程任务"
}
```

## 使用方法

### 基础使用

```python
from siyuan_api_client import SiYuanClient

# 初始化客户端
client = SiYuanClient(
    endpoint="http://YOUR_SERVER_IP:7000",
    token="YOUR_SIYUAN_TOKEN"
)

# 创建文档
doc_id = client.create_document(
    notebook_id="YOUR_NOTEBOOK_ID",
    path="/课程任务/第一章"
)

# 插入内容
client.insert_content(
    doc_id=doc_id,
    content="# 第一章内容\n\n这是第一章的详细内容..."
)
```

### 课程任务导入

```bash
# 导入课程任务到思源笔记
python3 course-task-to-siyuan.py --input /path/to/course/output

# 使用原始文件名导入
python3 course-task-to-siyuan-with-original-names.py --input /path/to/course/output

# 简化版导入
python3 course-task-to-siyuan-simple.py --input /path/to/course/output
```

### 会话归档

```bash
# 归档当前会话
python3 archive-current-session.py --session-id SESSION_ID
```

## API说明

### SiYuanClient 类

主要方法：

- `create_document()`: 创建新文档
- `insert_content()`: 插入内容
- `append_content()`: 追加内容
- `upload_asset()`: 上传资产文件
- `get_document()`: 获取文档内容
- `delete_document()`: 删除文档

## 输出格式

导入的课程任务将按照以下结构组织：

```
笔记本：课程任务
├── 第一章 社会工作服务通用模式
│   ├── 01_转写文本
│   ├── 02_预处理文本
│   ├── 04_考试经验
│   ├── 05_AI深度分析
│   └── 06_备考精华
├── 第二章 社会工作服务通用过程
│   └── ...
└── ...
```

## 部署要求

### 思源笔记服务

需要部署思源笔记服务端：

1. **Docker部署**：

```bash
docker run -d \
  --name siyuan \
  --restart always \
  -p 7000:6806 \
  b3log/siyuan:latest
```

2. **本地安装**：
下载并安装思源笔记：https://github.com/siyuan-note/siyuan

### 配置要求

- 思源笔记版本 >= 2.0.0
- 开启API服务（默认端口6806）
- 创建目标笔记本

## 注意事项

- 确保思源笔记API服务已启动
- API Token具有足够权限
- 笔记本ID正确
- 网络连接稳定

## 目录结构

```
siyuan-integration/
├── SKILL.md                              # 技能说明文档
├── README.md                             # 本文件
├── siyuan-api-client.py                  # API客户端
├── siyuan-config.json.example                    # 配置文件示例
├── course-task-to-siyuan.py             # 课程任务导入
├── course-task-to-siyuan-simple.py      # 简化版导入
├── course-task-to-siyuan-with-original-names.py  # 使用原始文件名导入
└── archive-current-session.py           # 会话归档
```

## 错误处理

- **连接失败**: 检查网络和API端点配置
- **认证失败**: 验证Token是否正确
- **权限错误**: 确认笔记本访问权限
- **文件上传失败**: 检查资产文件大小和格式

## 许可证

MIT License

## 作者

OpenClaw Community

## 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw)
- [思源笔记](https://github.com/siyuan-note/siyuan)