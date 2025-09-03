#!/usr/bin/env python3
"""
Google Document同期スクリプト
指定されたGoogle DocumentをローカルMarkdownファイルに同期
"""

import os
import sys
from datetime import datetime
from google_drive_manager import GoogleDriveManager, extract_file_id_from_url

def sync_document_to_markdown(document_url: str, output_dir: str = "../天郷事業/01_瞑想事業/瞑想YouTube"):
    """
    Google DocumentをMarkdownファイルに同期
    
    Args:
        document_url: Google DocumentのURL
        output_dir: 出力ディレクトリ
    """
    
    # URLからドキュメントIDを抽出
    document_id = extract_file_id_from_url(document_url)
    if not document_id:
        print(f"エラー: URLからドキュメントIDを抽出できませんでした: {document_url}")
        return False
    
    try:
        # Google Drive Managerを初期化
        print("Google Drive APIに接続中...")
        drive_manager = GoogleDriveManager()
        
        # ドキュメント内容を取得
        print(f"ドキュメントを取得中... ID: {document_id}")
        doc_data = drive_manager.get_document_content(document_id)
        
        if not doc_data:
            print("エラー: ドキュメントの取得に失敗しました")
            return False
        
        # ファイル名を生成（タイトルから安全なファイル名を作成）
        title = doc_data.get('title', 'untitled_document')
        safe_filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_filename = safe_filename.replace(' ', '_')
        
        # 出力ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)
        
        # Markdownファイルのパス
        markdown_path = os.path.join(output_dir, f"{safe_filename}.md")
        
        # Markdownコンテンツを作成
        markdown_content = f"""# {doc_data.get('title', 'Untitled')}

> **同期元:** [Google Document]({document_url})  
> **最終同期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **ドキュメントID:** {document_id}

---

{doc_data.get('content', '')}

---

*このファイルは Google Document から自動同期されています*
"""
        
        # ファイルに書き込み
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ 同期完了: {markdown_path}")
        print(f"📄 タイトル: {doc_data.get('title')}")
        print(f"📝 文字数: {len(doc_data.get('content', ''))}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def main():
    """メイン関数"""
    
    # デフォルトのドキュメントURL（瞑想YT_参考動画書き起こし）
    default_url = "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing"
    
    # コマンドライン引数からURLを取得（指定されていない場合はデフォルトを使用）
    document_url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    print("=== Google Document 同期ツール ===")
    print(f"対象URL: {document_url}")
    print()
    
    # 同期実行
    success = sync_document_to_markdown(document_url)
    
    if success:
        print("\n🎉 同期が正常に完了しました！")
    else:
        print("\n💥 同期に失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
