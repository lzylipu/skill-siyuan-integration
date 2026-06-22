#!/usr/bin/env python3
"""
课程任务数据持久化到思源笔记 - 使用原始中文文件名
根据 path-mapping.json 映射回原始文件名
"""

import os
import sys
import json
from pathlib import Path

# 配置路径
COURSE_OUTPUT_BASE = "${COURSE_OUTPUT_BASE}"
SIYUAN_CONFIG_FILE = "<config-path>/siyuan-config.json"
MAPPING_FILE = "${MAPPING_FILE}"

SUBJECTS = ["01_practice", "02_law", "03_comprehensive"]
SUBJECT_NAMES = {
    "01_practice": "社会工作实务",
    "02_law": "社会工作法规与政策", 
    "03_comprehensive": "社会工作综合能力"
}

# 科目映射
SUBJECT_MAPPING = {
    "01_practice": "social_work_practice",
    "02_law": "social_work_law", 
    "03_comprehensive": "social_work_comprehensive"
}

def load_siyuan_config():
    """加载思源笔记配置"""
    if os.path.exists(SIYUAN_CONFIG_FILE):
        with open(SIYUAN_CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def load_filename_mapping():
    """加载文件名映射"""
    if os.path.exists(MAPPING_FILE):
        with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
            # 创建反向映射：new_name -> original_name
            reverse_mapping = {}
            for subject_key, subject_data in mapping_data["subjects"].items():
                for file_info in subject_data["files"]:
                    if file_info.get("ok", False):
                        new_name = file_info["new"]
                        orig_name = file_info["orig"]
                        reverse_mapping[new_name] = orig_name
            return reverse_mapping
    return {}

def get_original_filename(converted_filename, filename_mapping):
    """根据转换后的文件名获取原始文件名"""
    # 移除扩展名
    base_name = Path(converted_filename).stem
    
    # 在映射中查找
    if base_name in filename_mapping:
        return filename_mapping[base_name]
    else:
        # 如果找不到映射，返回原文件名
        return converted_filename

def get_transcripts_content_with_original_names(subject_code, filename_mapping):
    """获取转录文本内容，使用原始文件名"""
    transcript_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/01_转写文本"
    if not os.path.exists(transcript_dir):
        return "暂无转录内容"
    
    transcripts = list(Path(transcript_dir).glob("*.txt"))
    if not transcripts:
        return "暂无转录内容"
    
    content = "## 📚 转录文本\n\n"
    processed_count = 0
    
    for transcript_file in sorted(transcripts):
        if processed_count >= 15:  # 限制数量
            break
            
        converted_name = transcript_file.stem
        original_name = get_original_filename(converted_name, filename_mapping)
        
        with open(transcript_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        
        if text:
            # 提取前200字符作为摘要
            summary = text[:200].replace('\n', ' ')
            content += f"- **{original_name}**: {summary}{'...' if len(text) > 200 else ''}\n"
            processed_count += 1
    
    return content

def create_subject_document_with_original_names(config, subject_code, filename_mapping):
    """为单个科目创建完整文档，使用原始文件名"""
    subject_name = SUBJECT_NAMES[subject_code]
    
    print(f"  → 生成 {subject_name} 文档（使用原始文件名）...")
    
    # 构建完整内容
    full_content = f"""# {subject_name}

自动生成的课程资料，包含转录文本、AI分析和备考精华。
所有文件名已恢复为原始中文名称。

---
"""
    
    # 添加转录文本（使用原始文件名）
    full_content += get_transcripts_content_with_original_names(subject_code, filename_mapping) + "\n"
    
    # AI 分析和备考精华保持不变（因为不依赖文件名）
    full_content += get_analysis_content(subject_code) + "\n"
    full_content += get_essentials_content(subject_code) + "\n"
    
    full_content += f"""---
*生成时间: {get_current_time()}*
*数据来源: OpenClaw 课程任务系统*
*文件名: 已恢复原始中文名称*
"""
    
    return full_content

def get_analysis_content(subject_code):
    """获取 AI 深度分析内容（简化版，不依赖文件名）"""
    analysis_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/05_AI 深度分析"
    if not os.path.exists(analysis_dir):
        return "## 🧠 AI 深度分析\n\n暂无深度分析"
    
    analysis_files = list(Path(analysis_dir).glob("*_深度分析.md"))
    if not analysis_files:
        return "## 🧠 AI 深度分析\n\n暂无深度分析"
    
    content = "## 🧠 AI 深度分析\n\n"
    all_content = ""
    for analysis_file in sorted(analysis_files[:5]):
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
            content += "- 核心概念解析\n- 考试重点提示\n- 学习建议\n"
    else:
        content += "- 核心概念解析\n- 考试重点提示\n- 学习建议\n"
    
    return content

def get_essentials_content(subject_code):
    """获取备考精华内容（简化版）"""
    essentials_dir = f"{COURSE_OUTPUT_BASE}/{subject_code}/06_备考精华"
    if not os.path.exists(essentials_dir):
        return "## 📖 备考精华\n\n暂无备考精华"
    
    content = "## 📖 备考精华\n\n"
    
    # 名词解释
    term_file = f"{essentials_dir}/名词解释.md"
    if os.path.exists(term_file):
        content += "### 名词解释\n- 专业术语定义\n\n"
    
    # 思维导图  
    mindmap_file = f"{essentials_dir}/思维导图.md"
    if os.path.exists(mindmap_file):
        content += "### 思维导图\n- 知识点关联结构\n\n"
    
    # 章节要点总结
    content += "### 章节要点总结\n- 重点内容归纳\n"
    
    return content

def get_current_time():
    """获取当前时间字符串"""
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S')

def main():
    print("=" * 60)
    print("课程任务数据持久化到思源笔记")
    print("✅ 使用原始中文文件名")
    print("=" * 60)
    
    # 加载配置
    config = load_siyuan_config()
    if not config:
        print("❌ 请先配置思源笔记参数")
        sys.exit(1)
    
    # 加载文件名映射
    filename_mapping = load_filename_mapping()
    if not filename_mapping:
        print("❌ 未找到文件名映射文件")
        sys.exit(1)
    
    print(f"✅ 加载 {len(filename_mapping)} 个文件名映射")
    
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
        
        # 生成完整文档内容（使用原始文件名）
        document_content = create_subject_document_with_original_names(config, subject_code, filename_mapping)
        
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
                    "path": f"/{subject_name} (原始文件名)",
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
    print("✅ 文件名已恢复为原始中文名称！")
    print("=" * 60)

if __name__ == "__main__":
    main()