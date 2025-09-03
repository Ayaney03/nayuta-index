#!/usr/bin/env python3
"""
スマートセクション抽出ツール
様々なパターンでドキュメントを分離
"""

import re
from google_drive_manager import GoogleDriveManager, extract_file_id_from_url

def analyze_content_patterns(content: str):
    """コンテンツのパターンを分析"""
    
    patterns = {
        "numbered_sections": len(re.findall(r'^\d{2}\s+', content, re.MULTILINE)),
        "horizontal_rules": len(re.findall(r'^[-=]{3,}$', content, re.MULTILINE)),
        "chapter_headers": len(re.findall(r'^チャプター\s*\d+', content, re.MULTILINE)),
        "title_headers": len(re.findall(r'^タイトル:', content, re.MULTILINE)),
        "video_sections": len(re.findall(r'https://www\.youtube\.com/watch', content)),
    }
    
    print("=== コンテンツパターン分析 ===")
    for pattern, count in patterns.items():
        print(f"{pattern}: {count}個")
    
    return patterns

def suggest_extraction_method(document_url: str):
    """最適な抽出方法を提案"""
    
    document_id = extract_file_id_from_url(document_url)
    if not document_id:
        return
    
    try:
        drive_manager = GoogleDriveManager()
        doc_data = drive_manager.get_document_content(document_id)
        content = doc_data.get('content', '')
        
        print(f"📄 ドキュメント: {doc_data.get('title')}")
        print(f"📝 総文字数: {len(content)}")
        print()
        
        patterns = analyze_content_patterns(content)
        
        print("\n=== 推奨抽出方法 ===")
        
        if patterns["numbered_sections"] > 1:
            print("✅ 数字セクション分離 (01, 02, 03...)")
            print("   コマンド: python3 extract_sections.py")
        
        elif patterns["title_headers"] > 1:
            print("✅ タイトル別分離")
            print("   複数の動画の書き起こしが含まれています")
        
        elif patterns["chapter_headers"] > 1:
            print("✅ チャプター別分離")
            print("   一つの動画の複数チャプターが含まれています")
        
        else:
            print("ℹ️  単一コンテンツ")
            print("   分離の必要はありませんが、手動で区切りを追加できます")
        
        print("\n=== 手動でタブ内容を追加する方法 ===")
        print("1. Google Docsで各タブの内容をコピー")
        print("2. 新しいGoogle Documentを作成")
        print("3. 以下のコマンドで追加:")
        print("   python3 auto_sync_documents.py add 'タブ名' 'https://docs.google.com/document/d/新しいID/edit'")
        
        # コンテンツのプレビューを表示
        print(f"\n=== コンテンツプレビュー ===")
        lines = content.split('\n')[:10]
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"{i:2d}: {line[:80]}...")
        
    except Exception as e:
        print(f"エラー: {e}")

def main():
    import sys
    
    default_url = "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing"
    document_url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    print("=== スマートセクション分析ツール ===")
    print(f"対象URL: {document_url}")
    print()
    
    suggest_extraction_method(document_url)

if __name__ == "__main__":
    main()
