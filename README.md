# 📝 SiYuan Note Integration / 思源笔记自动归档同步工具

> 🌐 English | [简体中文](./README.md)
> Persist files, text, and chat sessions to SiYuan note-taking database via REST APIs.
> 将课程任务、学习产出与当前 AI 会话自动持久化同步至自建思源笔记系统。

## ✨ 功能特性 / Features

- 📑 **文档创建 / Doc creation**: auto-generate markdown documents
- 📂 **资产管理 / Asset management**: upload images/attachments to asset storage
- 🔄 **会话归档 / Session Archiver**: dump conversation history as Markdown
- 🎓 **课程集成 / Course integration**: batch import lecture task data

## 🚀 安装 / Installation

```bash
pip install requests
```

Docker 部署思源笔记 / Deploy SiYuan:

```bash
docker run -d --name siyuan --restart always -p 7000:6806 b3log/siyuan:latest
```

配置环境变量 / Environment:

```bash
export SIYUAN_ENDPOINT="${SIYUAN_ENDPOINT}"
export SIYUAN_TOKEN="YOUR_SIYUAN_TOKEN"
export SIYUAN_NOTEBOOK="YOUR_NOTEBOOK_ID"
export SIYUAN_TARGET_PATH="/课程任务"
```

## 📖 使用方法 / Usage

```bash
# 导入课程任务 / Import course tasks
python3 course-task-to-siyuan.py --input /path/to/course/output

# 归档当前会话 / Archive session
python3 archive-current-session.py
```

## 📊 数据结构 / Data Structure

```
笔记本：课程任务
├── 第一章 社会工作服务通用模式
│   ├── 01_转写文本
│   ├── 02_预处理文本
│   ├── 04_考试经验
│   ├── 05_AI深度分析
│   └── 06_备考精华
└── ...
```

## ⚙️ 配置文件 / Configuration

```json
{
  "endpoint": "${SIYUAN_ENDPOINT}",
  "token": "YOUR_SIYUAN_TOKEN",
  "notebook_id": "YOUR_NOTEBOOK_ID",
  "target_path": "/课程任务"
}
```

## 🔧 错误处理 / Troubleshooting

| 错误 / Error | 原因 / Cause | 解决 / Solution |
|------|------|------|
| 连接失败 / Connection failed | API 未启动 / API down | 检查端口 / check port 6806 |
| 认证失败 / Auth failed | Token 错误 / wrong token | 验证 Token |
| 权限错误 / Permission | 笔记本访问 / notebook access | 确认权限设置 |

## 📁 目录结构 / Structure

```
siyuan-integration/
├── SKILL.md
├── README.md
├── siyuan-api-client.py
├── siyuan-config.json
├── course-task-to-siyuan.py
├── course-task-to-siyuan-simple.py
├── course-task-to-siyuan-with-original-names.py
└── archive-current-session.py
```

## 📄 许可证 / License

MIT
