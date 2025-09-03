#!/usr/bin/env python3
"""
Google Documents 自動同期システム
複数のGoogle Documentを定期的に同期するためのスクリプト
"""

import os
import time
import json
from datetime import datetime
from typing import List, Dict
from sync_document import sync_document_to_markdown

class DocumentSyncManager:
    """ドキュメント同期管理クラス"""
    
    def __init__(self, config_file: str = "sync_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """設定ファイルを読み込み"""
        default_config = {
            "documents": [
                {
                    "name": "瞑想YT_参考動画書き起こし",
                    "url": "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing",
                    "output_dir": "../天郷事業/01_瞑想事業/瞑想YouTube",
                    "enabled": True
                }
            ],
            "sync_interval_minutes": 30,
            "auto_sync": False
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"設定ファイル読み込みエラー: {e}")
                return default_config
        else:
            # デフォルト設定を保存
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict = None):
        """設定ファイルを保存"""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"設定ファイル保存エラー: {e}")
    
    def add_document(self, name: str, url: str, output_dir: str = "../天郷事業/01_瞑想事業/瞑想YouTube"):
        """新しいドキュメントを追加"""
        new_doc = {
            "name": name,
            "url": url,
            "output_dir": output_dir,
            "enabled": True
        }
        
        self.config["documents"].append(new_doc)
        self.save_config()
        print(f"✅ ドキュメントを追加しました: {name}")
    
    def sync_all_documents(self) -> bool:
        """すべての有効なドキュメントを同期"""
        success_count = 0
        total_count = 0
        
        print(f"\n=== 一括同期開始 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ===")
        
        for doc in self.config["documents"]:
            if not doc.get("enabled", True):
                continue
                
            total_count += 1
            print(f"\n📄 同期中: {doc['name']}")
            
            success = sync_document_to_markdown(
                doc["url"], 
                doc.get("output_dir", "../天郷事業/01_瞑想事業/瞑想YouTube")
            )
            
            if success:
                success_count += 1
            
            # 連続リクエストを避けるため少し待機
            time.sleep(1)
        
        print(f"\n=== 同期完了 ===")
        print(f"成功: {success_count}/{total_count}")
        
        return success_count == total_count
    
    def start_auto_sync(self):
        """自動同期を開始"""
        if not self.config.get("auto_sync", False):
            print("自動同期は無効になっています。sync_config.json で auto_sync を true に設定してください。")
            return
        
        interval_minutes = self.config.get("sync_interval_minutes", 30)
        print(f"🔄 自動同期を開始します（間隔: {interval_minutes}分）")
        print("Ctrl+C で停止")
        
        try:
            while True:
                self.sync_all_documents()
                
                print(f"\n⏰ {interval_minutes}分後に次回同期...")
                time.sleep(interval_minutes * 60)
                
        except KeyboardInterrupt:
            print("\n🛑 自動同期を停止しました")
    
    def list_documents(self):
        """登録されているドキュメント一覧を表示"""
        print("\n=== 登録ドキュメント一覧 ===")
        
        for i, doc in enumerate(self.config["documents"], 1):
            status = "✅" if doc.get("enabled", True) else "❌"
            print(f"{i}. {status} {doc['name']}")
            print(f"   URL: {doc['url']}")
            print(f"   出力先: {doc.get('output_dir', '../天郷事業/01_瞑想事業/瞑想YouTube')}")
            print()

def main():
    """メイン関数"""
    import sys
    
    manager = DocumentSyncManager()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python auto_sync_documents.py sync          # 一回だけ同期")
        print("  python auto_sync_documents.py auto          # 自動同期開始")
        print("  python auto_sync_documents.py list          # ドキュメント一覧")
        print("  python auto_sync_documents.py add <name> <url> [output_dir]  # ドキュメント追加")
        return
    
    command = sys.argv[1].lower()
    
    if command == "sync":
        manager.sync_all_documents()
    
    elif command == "auto":
        manager.start_auto_sync()
    
    elif command == "list":
        manager.list_documents()
    
    elif command == "add":
        if len(sys.argv) < 4:
            print("エラー: ドキュメント名とURLが必要です")
            print("使用例: python auto_sync_documents.py add '新しいドキュメント' 'https://docs.google.com/...'")
            return
        
        name = sys.argv[2]
        url = sys.argv[3]
        output_dir = sys.argv[4] if len(sys.argv) > 4 else "../天郷事業/01_瞑想事業/瞑想YouTube"
        
        manager.add_document(name, url, output_dir)
    
    else:
        print(f"不明なコマンド: {command}")

if __name__ == "__main__":
    main()
