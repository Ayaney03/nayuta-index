#!/usr/bin/env python3
"""
Google Document構造解析スクリプト
ドキュメント内のタブやセクションの構造を詳しく調べる
"""

import json
from google_drive_manager import GoogleDriveManager, extract_file_id_from_url

def analyze_document_structure(document_url: str):
    """
    Google Documentの詳細構造を解析
    
    Args:
        document_url: Google DocumentのURL
    """
    
    # URLからドキュメントIDを抽出
    document_id = extract_file_id_from_url(document_url)
    if not document_id:
        print(f"エラー: URLからドキュメントIDを抽出できませんでした: {document_url}")
        return
    
    try:
        # Google Drive Managerを初期化
        print("Google Drive APIに接続中...")
        drive_manager = GoogleDriveManager()
        
        # ドキュメント内容を取得
        print(f"ドキュメントを取得中... ID: {document_id}")
        doc_data = drive_manager.get_document_content(document_id)
        
        if not doc_data:
            print("エラー: ドキュメントの取得に失敗しました")
            return
        
        # 完全なドキュメント構造を取得
        full_document = doc_data.get('full_document', {})
        
        print(f"\n=== ドキュメント基本情報 ===")
        print(f"タイトル: {doc_data.get('title')}")
        print(f"ドキュメントID: {document_id}")
        print(f"リビジョンID: {doc_data.get('revision_id')}")
        
        # ドキュメントの構造を詳しく調べる
        print(f"\n=== ドキュメント構造解析 ===")
        
        # タブ情報を探す
        tabs = full_document.get('tabs', [])
        if tabs:
            print(f"📑 タブ数: {len(tabs)}")
            for i, tab in enumerate(tabs):
                print(f"\n--- タブ {i+1} ---")
                print(f"ID: {tab.get('tabId', 'N/A')}")
                
                # タブのプロパティを確認
                tab_properties = tab.get('tabProperties', {})
                print(f"タイトル: {tab_properties.get('title', 'Untitled')}")
                print(f"インデックス: {tab_properties.get('index', 'N/A')}")
                
                # 各タブの内容を取得
                child_tabs = tab.get('childTabs', [])
                if child_tabs:
                    print(f"子タブ数: {len(child_tabs)}")
                
                # タブ内のコンテンツを確認
                document_tab = tab.get('documentTab', {})
                if document_tab:
                    body = document_tab.get('body', {})
                    content = body.get('content', [])
                    print(f"コンテンツ要素数: {len(content)}")
                    
                    # テキスト内容を抽出
                    tab_text = ""
                    for element in content:
                        if 'paragraph' in element:
                            for text_run in element['paragraph'].get('elements', []):
                                if 'textRun' in text_run:
                                    tab_text += text_run['textRun'].get('content', '')
                    
                    print(f"テキスト文字数: {len(tab_text)}")
                    if tab_text.strip():
                        # 最初の100文字を表示
                        preview = tab_text.strip()[:100].replace('\n', ' ')
                        print(f"プレビュー: {preview}...")
        else:
            print("❌ タブ情報が見つかりませんでした")
            
            # 従来の方法でボディを確認
            body = full_document.get('body', {})
            content = body.get('content', [])
            print(f"📄 メインボディのコンテンツ要素数: {len(content)}")
        
        # 詳細構造をJSONファイルに保存
        output_file = f"document_structure_{document_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(full_document, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 詳細構造を保存しました: {output_file}")
        
        # 利用可能なキーを表示
        print(f"\n=== ドキュメントの主要キー ===")
        for key in full_document.keys():
            print(f"- {key}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

def main():
    """メイン関数"""
    import sys
    
    # デフォルトのドキュメントURL
    default_url = "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing"
    
    document_url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    print("=== Google Document 構造解析ツール ===")
    print(f"対象URL: {document_url}")
    print()
    
    analyze_document_structure(document_url)

if __name__ == "__main__":
    main()
