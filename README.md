# SiYuan Integration - OpenClaw Skill

**[English](./README.en.md) | 中文**

思源笔记集成技能，将课程任务数据持久化到思源笔记系统。

## 功能特性

- **文档创建**: 在思源笔记中创建新文档
- **内容插入**: 向现有文档插入内容
- **资产管理**: 上传和管理文件资产
- **会话归档**: 自动归档当前会话内容
- **课程任务集成**: 专门针对课程任务的数据导入

## 安装

### 1. 安装依赖

```bash
pip install requests
```

### 2. 部署思源笔记服务

**Docker部署（推荐）**：

```bash
docker run -d \
  --name siyuan \
  --restart always \
  -p 7000:6806 \
  b3log/siyuan:latest
```

**本地安装**：

下载并安装思源笔记：https://github.com/siyuan-note/siyuan

### 3. 配置环境变量

```bash
export SIYUAN_ENDPOINT="${SIYUAN_ENDPOINT}"
export SIYUAN_TOKEN="YOUR_SIYUAN_TOKEN"
export SIYUAN_NOTEBOOK="YOUR_NOTEBOOK_ID"
export SIYUAN_TARGET_PATH="/课程任务"
```

### 4. 安装到OpenClaw

```bash
cp -r siyuan-integration /path/to/openclaw/skills/
```

## 使用方法

### Python API使用

```python
from siyuan_api_client import SiYuanClient

# 初始化客户端
client = SiYuanClient()

# 创建文档
doc_id = client.create_document(
    notebook_id="YOUR_NOTEBOOK_ID",
    path="/课程任务/第一章"
)

# 插入内容
client.insert_content(
    doc_id=doc_id,
    content="# 第一章内容\n\n详细内容..."
)
```

### 命令行使用

```bash
# 导入课程任务
python3 course-task-to-siyuan.py --input /path/to/course/output

# 使用原始文件名导入
python3 course-task-to-siyuan-with-original-names.py --input /path/to/course/output

# 归档当前会话
python3 archive-current-session.py
```

### OpenClaw对话中使用

```
用户: 把课程内容导入思源笔记
AI: 正在导入课程任务到思源笔记...
    ✅ 已导入第一章
    ✅ 已导入第二章
    ...
    完成！共导入18个章节
```

## 支持的操作

| 操作 | 说明 | 方法 |
|------|------|------|
| **创建文档** | 创建新的思源笔记文档 | `create_document()` |
| **插入内容** | 在文档中插入Markdown内容 | `insert_content()` |
| **追加内容** | 在文档末尾追加内容 | `append_content()` |
| **上传资产** | 上传文件到思源资产库 | `upload_asset()` |
| **获取文档** | 获取文档内容 | `get_document()` |
| **删除文档** | 删除指定文档 | `delete_document()` |

## 数据结构

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

## 配置文件

使用 `siyuan-config.json` 配置：

```json
{
  "endpoint": "${SIYUAN_ENDPOINT}",
  "token": "YOUR_SIYUAN_TOKEN",
  "notebook_id": "YOUR_NOTEBOOK_ID",
  "target_path": "/课程任务"
}
```

## API参考

### SiYuanClient

```python
class SiYuanClient:
    def __init__(self, endpoint: str, token: str = ""):
        """初始化客户端"""

    def create_document(self, notebook_id: str, path: str) -> str:
        """创建文档，返回文档ID"""

    def insert_content(self, doc_id: str, content: str) -> bool:
        """插入内容"""

    def append_content(self, doc_id: str, content: str) -> bool:
        """追加内容"""

    def upload_asset(self, file_path: str) -> str:
        """上传资产文件，返回资产路径"""

    def get_document(self, doc_id: str) -> dict:
        """获取文档内容"""

    def delete_document(self, doc_id: str) -> bool:
        """删除文档"""
```

## 错误处理

| 错误类型 | 原因 | 解决方法 |
|---------|------|----------|
| **连接失败** | API服务未启动 | 检查网络和端口配置 |
| **认证失败** | Token错误 | 验证Token是否正确 |
| **权限错误** | 笔记本访问权限 | 确认笔记本权限设置 |
| **文件上传失败** | 文件大小或格式 | 检查文件大小限制 |

## 目录结构

```
siyuan-integration/
├── SKILL.md                              # 技能说明
├── README.md                             # 本文件
├── siyuan-api-client.py                  # API客户端
├── siyuan-config.json                    # 配置示例
├── course-task-to-siyuan.py             # 课程任务导入
├── course-task-to-siyuan-simple.py      # 简化版导入
├── course-task-to-siyuan-with-original-names.py  # 原始文件名导入
└── archive-current-session.py           # 会话归档
```

## 注意事项

- 确保思源笔记API服务已启动（默认端口6806）
- API Token需要具有笔记本访问权限
- 大量文件导入时注意API频率限制
- 建议先在测试笔记本中验证

## 技术实现

- **Python 3** - 主要编程语言
- **requests** - HTTP请求库
- **思源笔记API** - 文档和资产管理

## 许可证

MIT License

## 作者

OpenClaw Community

## 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw)
- [思源笔记](https://github.com/siyuan-note/siyuan)