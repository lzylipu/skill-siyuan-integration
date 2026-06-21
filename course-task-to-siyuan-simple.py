#!/usr/bin/env python3
"""
课程任务数据持久化到思源笔记 - 简化版本
每个科目一个文档，包含所有相关内容
"""

import os
import sys
import json
from pathlib import Path

# 配置路径
COURSE_OUTPUT_BASE = "/vol02/1000-0-f9fae032/同步/课程-output"
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
            return json.load(f)
    return None

def get_transcripts_content(subject_code):
    """获取转录文本内容"""
    transcript_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/01_转写文本"
    if not os.path.exists(transcript_dir):
        return "暂无转录内容"
    
    transcripts = list(Path(transcript_dir).glob("*.txt"))
    if not transcripts:
        return "暂无转录内容"
    
    content = "## 📚 转录文本\n\n"
    for transcript_file in sorted(transcripts[:15]):  # 限制数量避免过长
        filename = transcript_file.stem
        with open(transcript_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if text:
            # 提取前200字符作为摘要
            summary = text[:200].replace('\n', ' ')
            content += f"- **{filename}**: {summary}{'...' if len(text) > 200 else ''}\n"
    
    return content

def get_analysis_content(subject_code):
    """获取 AI 深度分析内容"""
    analysis_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/05_AI 深度分析"
    if not os.path.exists(analysis_dir):
        return "暂无深度分析"
    
    analysis_files = list(Path(analysis_dir).glob("*_深度分析.md"))
    if not analysis_files:
        return "暂无深度分析"
    
    content = "## 🧠 AI 深度分析\n\n"
    # 合并所有分析内容的核心要点
    all_content = ""
    for analysis_file in sorted(analysis_files[:10]):  # 限制数量
        with open(analysis_file, 'r', encoding='utf-8') as f:
            analysis_text = f.read()
        all_content += analysis_text + "\n"
    
    # 提取核心内容
    if "讲课核心内容" in all_content:
        start = all_content.find("## 📚 讲课核心内容")
        end = all_content.find("## 🎯 考试重点提示")
        if start != -1 and end != -1:
            core_content = all_content[start:end]
            content += core_content + "\n"
        else:
            content += "核心概念和要点分析\n"
    else:
        content += "核心概念和要点分析\n"
    
    if "考试重点提示" in all_content:
        start = all_content.find("## 🎯 考试重点提示")
        end = all_content.find("## 📝 学习建议")
        if start != -1:
            exam_content = all_content[start:end] if end != -1 else all_content[start:]
            content += exam_content + "\n"
        else:
            content += "## 🎯 考试重点提示\n- 答题技巧和重点考点\n"
    else:
        content += "## 🎯 考试重点提示\n- 答题技巧和重点考点\n"
    
    return content

def get_essentials_content(subject_code):
    """获取备考精华内容"""
    essentials_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/06_备考精华"
    if not os.path.exists(essentials_dir):
        return "暂无备考精华"
    
    content = "## 📖 备考精华\n\n"
    
    # 名词解释
    term_file = f"{essentials_dir}/名词解释.md"
    if os.path.exists(term_file):
        with open(term_file, 'r', encoding='utf-8') as f:
            terms = f.read()
        if "名词解释" in terms:
            content += "### 名词解释\n"
            # 提取前5个术语
            lines = terms.split('\n')
            term_count = 0
            for line in lines:
                if line.startswith('### ') and term_count < 5:
                    content += line + "\n"
                    term_count += 1
                elif term_count >= 5:
                    break
            content += "\n"
    
    # 思维导图
    mindmap_file = f"{essentials_dir}/思维导图.md"
    if os.path.exists(mindmap_file):
        with open(mindmap_file, 'r', encoding='utf-8') as f:
            mindmap = f.read()
        if "思维导图" in mindmap:
            content += "### 思维导图\n知识点关联结构\n\n"
    
    # 章节要点总结
    summary_file = f"{essentials_dir}/章节知识要点总结.md"
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = f.read()
        if "知识要点归纳总结" in summary:
            content += "### 章节要点总结\n"
            # 提取关键要点
            lines = summary.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('### ') and '重点' in line:
                    content += line + "\n"
                    # 添加接下来的几个要点
                    for j in range(1, 4):
                        if i+j < len(lines) and lines[i+j].startswith('- '):
                            content += lines[i+j] + "\n"
                        else:
                            break
                    content += "\n"
                    break
    
    if content == "## 📖 备考精华\n\n":
        content += "备考要点、名词解释和思维导图\n"
    
    return content

def create_subject_document(config, subject_code):
    """为单个科目创建完整文档"""
    subject_name = SUBJECT_NAMES[subject_code]
    
    print(f"  → 生成 {subject_name} 文档...")
    
    # 构建完整内容
    full_content = f"""# {subject_name}

自动生成的课程资料，包含转录文本、AI分析和备考精华。

---
"""
    
    # 添加转录文本
    full_content += get_transcripts_content(subject_code) + "\n"
    
    # 添加 AI 深度分析
    full_content += get_analysis_content(subject_code) + "\n"
    
    # 添加备考精华
    full_content += get_essentials_content(subject_code) + "\n"
    
    full_content += f"""---
*生成时间: {get_current_time()}*
*数据来源: OpenClaw 课程任务系统*
"""
    
    return full_content

def get_current_time():
    """获取当前时间字符串"""
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("=" * 60)
    print("课程任务数据持久化到思源笔记 (简化版)")
    print("每个科目一个完整文档")
    print("=" * 60)
    
    # 加载配置
    config = load_siyuan_config()
    if not config:
        print("❌ 请先配置思源笔记参数")
        sys.exit(1)
    
    # 测试连接
    import requests
    try:
        resp = requests.post(
            f"{config['endpoint']}/api/system/version",
            headers={"Authorization": f"Token {config['token']}"},
            json={},
            timeout=10
        )
        if resp.status_code == 200 and resp.json().get("code") == 0:
            print("✅ 思源笔记连接成功")
        else:
            print("❌ 思源笔记连接失败")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 连接异常: {e}")
        sys.exit(1)
    
    # 为每个科目创建文档
    for subject_code in SUBJECTS:
        subject_name = SUBJECT_NAMES[subject_code]
        print(f"\n处理科目: {subject_name}")
        
        # 生成完整文档内容
        document_content = create_subject_document(config, subject_code)
        
        # 创建文档
        try:
            resp = requests.post(
                f"{config['endpoint']}/api/filetree/createDocWithMd",
                headers={
                    "Authorization": f"Token {config['token']}",
                    "Content-Type": "application/json"
                },
                json={
                    "notebook": config["notebook_id"],
                    "path": f"/{subject_name}",
                    "markdown": document_content
                },
                timeout=30
            )
            
            if resp.status_code == 200 and resp.json().get("code") == 0:
                doc_id = resp.json().get("data")
                print(f"  ✓ {subject_name} 文档创建成功 (ID: {doc_id})")
            else:
                print(f"  ❌ {subject_name} 文档创建失败")
                
        except Exception as e:
            print(f"  ❌ 创建异常: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 所有科目文档已创建完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()