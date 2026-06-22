#!/usr/bin/env python3
"""
思源笔记 API 客户端 - 用于课程任务数据持久化
支持文档创建、内容插入、资产上传等操作
"""

import os
import sys
import json
import requests
from typing import Optional, Dict, Any

# ==================== 配置区域 ====================
SIYUAN_ENDPOINT = os.environ.get("SIYUAN_ENDPOINT", "http://localhost:6806")
SIYUAN_TOKEN = os.environ.get("SIYUAN_TOKEN", "")
SIYUAN_NOTEBOOK = os.environ.get("SIYUAN_NOTEBOOK", "")  # 笔记本ID
SIYUAN_TARGET_PATH = os.environ.get("SIYUAN_TARGET_PATH", "/课程任务")  # 目标路径

class SiYuanClient:
    """
    思源笔记 API 客户端
    支持完整的文档管理和内容操作
    """
    
    def __init__(self, endpoint: str, token: str, notebook_id: str = "", target_path: str = "/课程任务"):
        self.endpoint = endpoint.rstrip("/")
        self.token = token
        self.notebook_id = notebook_id
        self.target_path = target_path
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, data: dict = None) -> Optional[Dict[str, Any]]:
        """通用请求方法"""
        try:
            url = f"{self.endpoint}{endpoint}"
            if method.upper() == "POST":
                resp = self.session.post(url, json=data, timeout=30)
            elif method.upper() == "GET":
                resp = self.session.get(url, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if resp.status_code == 200:
                result = resp.json()
                if result.get("code") == 0:
                    return result.get("data")
                else:
                    print(f"❌ API 错误: {result.get('msg', 'Unknown error')}")
                    return None
            else:
                print(f"❌ HTTP 错误: {resp.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def list_notebooks(self) -> list:
        """获取笔记本列表"""
        data = self._make_request("POST", "/api/notebook/lsNotebooks")
        if data and "notebooks" in data:
            return data["notebooks"]
        return []
    
    def create_document(self, title: str, content: str, path: str = None) -> Optional[str]:
        """
        创建新文档
        返回文档ID
        """
        if not self.notebook_id:
            print("❌ 未设置笔记本ID")
            return None
        
        if path is None:
            path = f"{self.target_path}/{title}"
        
        payload = {
            "notebook": self.notebook_id,
            "path": path,
            "markdown": content
        }
        
        doc_id = self._make_request("POST", "/api/filetree/createDocWithMd", payload)
        if doc_id:
            print(f"  ✓ 文档创建成功: {title} (ID: {doc_id})")
            return doc_id
        return None
    
    def insert_block(self, parent_id: str, content: str, data_type: str = "markdown") -> Optional[str]:
        """
        在指定位置插入内容块
        """
        payload = {
            "dataType": data_type,
            "data": content,
            "parentID": parent_id
        }
        
        result = self._make_request("POST", "/api/block/appendBlock", payload)
        if result and len(result) > 0:
            block_id = result[0]["doOperations"][0]["action"]["id"]
            print(f"  ✓ 内容块插入成功 (ID: {block_id})")
            return block_id
        return None
    
    def upload_asset(self, file_path: str, assets_dir: str = "/assets/") -> Optional[str]:
        """
        上传资产文件
        返回上传后的文件路径
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file[]': f}
                data = {'assetsDirPath': assets_dir}
                
                url = f"{self.endpoint}/api/asset/upload"
                resp = self.session.post(url, files=files, data=data, timeout=60)
                
                if resp.status_code == 200:
                    result = resp.json()
                    if result.get("code") == 0:
                        succ_map = result.get("data", {}).get("succMap", {})
                        if succ_map:
                            asset_path = list(succ_map.values())[0]
                            print(f"  ✓ 资产上传成功: {asset_path}")
                            return asset_path
                print(f"❌ 资产上传失败: {resp.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 资产上传异常: {e}")
            return None

def main():
    if len(sys.argv) < 2:
        print("用法：python3 siyuan-api-client.py <操作> [参数]")
        print("\n支持的操作:")
        print("  list-notebooks              - 列出所有笔记本")
        print("  create-doc <标题> <内容文件> - 创建文档")
        print("  upload-asset <文件路径>      - 上传资产")
        sys.exit(1)
    
    operation = sys.argv[1]
    
    # 初始化客户端
    client = SiYuanClient(SIYUAN_ENDPOINT, SIYUAN_TOKEN, SIYUAN_NOTEBOOK, SIYUAN_TARGET_PATH)
    
    if operation == "list-notebooks":
        notebooks = client.list_notebooks()
        if notebooks:
            print("可用笔记本:")
            for nb in notebooks:
                print(f"  - {nb['name']} (ID: {nb['id']})")
        else:
            print("❌ 未找到笔记本")
    
    elif operation == "create-doc":
        if len(sys.argv) < 4:
            print("用法: create-doc <标题> <内容文件>")
            sys.exit(1)
        
        title = sys.argv[2]
        content_file = sys.argv[3]
        
        if not os.path.exists(content_file):
            print(f"❌ 文件不存在: {content_file}")
            sys.exit(1)
        
        with open(content_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc_id = client.create_document(title, content)
        if doc_id:
            print(f"✅ 文档创建成功!")
        else:
            print("❌ 文档创建失败!")
    
    elif operation == "upload-asset":
        if len(sys.argv) < 3:
            print("用法: upload-asset <文件路径>")
            sys.exit(1)
        
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            sys.exit(1)
        
        asset_path = client.upload_asset(file_path)
        if asset_path:
            print(f"✅ 资产上传成功!")
        else:
            print("❌ 资产上传失败!")
    
    else:
        print(f"❌ 不支持的操作: {operation}")

if __name__ == "__main__":
    main()