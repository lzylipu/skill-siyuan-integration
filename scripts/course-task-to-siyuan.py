#!/usr/bin/env python3
"""
课程任务数据持久化到思源笔记
将 AI 深度分析结果、转录文本等保存到思源笔记中
"""

import os
import sys
import json
from pathlib import Path
from siyuan_api_client import SiYuanClient

# 配置路径
COURSE_OUTPUT_BASE = "${COURSE_OUTPUT_BASE}"
SIYUAN_CONFIG_FILE = "<config-path>/siyuan-config.json"

SUBJECTS = ["01_practice", "02_law", "03_comprehensive"]
SUBJECT_NAMES = {
    "01_practice": "社会工作实务",
    "02_law": "社会工作法规与政策", 
    "03_comprehensive": "社会工作综合能力"
}

def load_siyuan_config():
    """加载思源笔记配置"""
    if os.path.exists(SIYUAN_CONFIG_FILE):
        with open(SIYUAN_CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 强制使用配置文件中的值，忽略环境变量
            return config
    else:
        # 创建默认配置文件
        default_config = {
            "endpoint": "${SIYUAN_ENDPOINT}",
            "token": "a3frmq4jlzz20ib6",
            "notebook_id": "",
            "target_path": "/OpenClaw"
        }
        with open(SIYUAN_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"请编辑配置文件: {SIYUAN_CONFIG_FILE}")
        return None

def create_subject_structure(client, subject_code):
    """为每个科目创建思源笔记结构"""
    subject_name = SUBJECT_NAMES[subject_code]
    
    # 创建主文档
    main_content = f"""# {subject_name} 课程资料

## 📚 资料目录
- [转录文本](#{subject_code}-transcripts)
- [AI 深度分析](#{subject_code}-analysis)  
- [备考精华](#{subject_code}-essentials)

---
*自动生成于 {get_current_time()}*
"""
    
    doc_id = client.create_document(subject_name, main_content)
    return doc_id

def save_transcripts_to_siyuan(client, subject_code, parent_doc_id):
    """保存转录文本到思源笔记"""
    transcript_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/01_转写文本"
    if not os.path.exists(transcript_dir):
        return
    
    transcripts = list(Path(transcript_dir).glob("*.txt"))
    if not transcripts:
        return
    
    content = f"## {SUBJECT_NAMES[subject_code]} - 转录文本\n\n"
    
    for transcript_file in sorted(transcripts[:10]):  # 先处理前10个
        filename = transcript_file.stem
        with open(transcript_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if text:
            content += f"### {filename}\n\n```\n{text[:500]}{'...' if len(text) > 500 else ''}\n```\n\n"
    
    if parent_doc_id:
        client.insert_block(parent_doc_id, content)
    else:
        client.create_document(f"{SUBJECT_NAMES[subject_code]}-转录文本", content)

def save_analysis_to_siyuan(client, subject_code, parent_doc_id):
    """保存 AI 深度分析到思源笔记"""
    analysis_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/05_AI 深度分析"
    if not os.path.exists(analysis_dir):
        return
    
    analysis_files = list(Path(analysis_dir).glob("*_深度分析.md"))
    if not analysis_files:
        return
    
    content = f"## {SUBJECT_NAMES[subject_code]} - AI 深度分析\n\n"
    
    for analysis_file in sorted(analysis_files[:5]):  # 先处理前5个
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_content = f.read()
        
        content += f"{analysis_content}\n\n---\n\n"
    
    if parent_doc_id:
        client.insert_block(parent_doc_id, content)
    else:
        client.create_document(f"{SUBJECT_NAMES[subject_code]}-AI分析", content)

def save_essentials_to_siyuan(client, subject_code, parent_doc_id):
    """保存备考精华到思源笔记"""
    essentials_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/06_备考精华"
    if not os.path.exists(essentials_dir):
        return
    
    essentials_files = [
        "名词解释.md",
        "思维导图.md", 
        "章节知识要点总结.md"
    ]
    
    content = f"## {SUBJECT_NAMES[subject_code]} - 备考精华\n\n"
    
    for filename in essentials_files:
        file_path = f"{essentials_dir}/{filename}"
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            content += f"{file_content}\n\n---\n\n"
    
    if parent_doc_id:
        client.insert_block(parent_doc_id, content)
    else:
        client.create_document(f"{SUBJECT_NAMES[subject_code]}-备考精华", content)

def get_current_time():
    """获取当前时间字符串"""
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("=" * 60)
    print("课程任务数据持久化到思源笔记")
    print("=" * 60)
    
    # 加载配置
    config = load_siyuan_config()
    if not config:
        print("❌ 请先配置思源笔记参数")
        sys.exit(1)
    
    # 初始化客户端
    client = SiYuanClient(
        endpoint=config["endpoint"],
        token=config["token"], 
        notebook_id=config["notebook_id"],
        target_path=config["target_path"]
    )
    
    # 验证连接
    notebooks = client.list_notebooks()
    if not notebooks:
        print("❌ 无法连接到思源笔记，请检查配置")
        sys.exit(1)
    
    print(f"✅ 连接到思源笔记，找到 {len(notebooks)} 个笔记本")
    
    # 为每个科目处理数据
    for subject_code in SUBJECTS:
        print(f"\n处理科目: {SUBJECT_NAMES[subject_code]}")
        
        # 创建主文档结构
        main_doc_id = create_subject_structure(client, subject_code)
        
        # 保存转录文本
        print("  → 保存转录文本...")
        save_transcripts_to_siyuan(client, subject_code, main_doc_id)
        
        # 保存 AI 深度分析
        print("  → 保存 AI 深度分析...")
        save_analysis_to_siyuan(client, subject_code, main_doc_id)
        
        # 保存备考精华
        print("  → 保存备考精华...")
        save_essentials_to_siyuan(client, subject_code, main_doc_id)
        
        print(f"  ✓ {SUBJECT_NAMES[subject_code]} 处理完成")
    
    print("\n" + "=" * 60)
    print("✅ 所有课程任务数据已持久化到思源笔记！")
    print("=" * 60)

if __name__ == "__main__":
    main()