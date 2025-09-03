#!/usr/bin/env python3
"""
Google Document セクション分離スクリプト
ドキュメント内の複数の文字起こしを自動的に分離・整理
"""

import os
import re
from datetime import datetime
from google_drive_manager import GoogleDriveManager, extract_file_id_from_url

def extract_sections_from_document(document_url: str, output_dir: str = "../天郷事業/01_瞑想事業/瞑想YouTube"):
    """
    Google Documentから複数のセクションを抽出して個別ファイルに保存
    
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
        
        content = doc_data.get('content', '')
        title = doc_data.get('title', 'untitled_document')
        
        print(f"\n=== ドキュメント解析 ===")
        print(f"タイトル: {title}")
        print(f"総文字数: {len(content)}")
        
        # セクションを分離するためのパターンを定義
        # 数字で始まる行（01, 02, 03など）をセクション区切りとして使用
        section_pattern = r'^(\d{2})\s+(.+?)(?=^\d{2}\s+|\Z)'
        
        # セクションを抽出
        sections = re.findall(section_pattern, content, re.MULTILINE | re.DOTALL)
        
        if not sections:
            # 別のパターンを試す：横線や特定のキーワードで区切り
            print("数字パターンが見つかりません。別の区切り方法を試します...")
            
            # 横線（---）やページブレイクで分割
            parts = re.split(r'\n\s*[-=]{3,}\s*\n|\n\s*\n\s*\n', content)
            sections = []
            
            for i, part in enumerate(parts, 1):
                part = part.strip()
                if len(part) > 50:  # 十分な長さのセクションのみ
                    # セクションタイトルを抽出（最初の行または最初の文）
                    lines = part.split('\n')
                    section_title = lines[0].strip() if lines else f"セクション{i:02d}"
                    
                    # タイトルが長すぎる場合は短縮
                    if len(section_title) > 50:
                        section_title = section_title[:47] + "..."
                    
                    sections.append((f"{i:02d}", f"{section_title}\n\n{part}"))
        
        if not sections:
            print("❌ セクションを分離できませんでした。全体を一つのファイルとして保存します。")
            sections = [("01", f"{title}\n\n{content}")]
        
        print(f"📑 {len(sections)}個のセクションを検出しました")
        
        # 出力ディレクトリを作成
        os.makedirs(output_dir, exist_ok=True)
        
        # 各セクションを個別ファイルに保存
        saved_files = []
        
        for section_num, section_content in sections:
            # セクションタイトルを抽出（最初の行）
            lines = section_content.strip().split('\n')
            section_title = lines[0].strip() if lines else f"セクション{section_num}"
            
            # ファイル名を生成（安全な文字のみ使用）
            safe_title = re.sub(r'[^\w\s-]', '', section_title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            safe_title = safe_title[:50]  # 長さ制限
            
            filename = f"{section_num}_{safe_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Markdownコンテンツを作成
            markdown_content = f"""# {section_title}

> **同期元:** [Google Document]({document_url})  
> **セクション:** {section_num}  
> **最終同期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **ドキュメントID:** {document_id}

---

{section_content.strip()}

---

*このファイルは Google Document から自動抽出されました*
"""
            
            # ファイルに書き込み
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            saved_files.append(filepath)
            print(f"✅ セクション{section_num}: {filename}")
            print(f"   文字数: {len(section_content)}")
            print(f"   ファイル: {filepath}")
            print()
        
        # インデックスファイルを作成
        index_content = f"""# {title} - セクション一覧

> **同期元:** [Google Document]({document_url})  
> **最終同期:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **総セクション数:** {len(sections)}

## 📑 セクション一覧

"""
        
        for i, (section_num, section_content) in enumerate(sections, 1):
            lines = section_content.strip().split('\n')
            section_title = lines[0].strip() if lines else f"セクション{section_num}"
            filename = saved_files[i-1].split('/')[-1]
            
            index_content += f"{i}. **[{section_title}](./{filename})**\n"
            index_content += f"   - セクション番号: {section_num}\n"
            index_content += f"   - 文字数: {len(section_content)}\n\n"
        
        index_content += f"""
---

*このインデックスは Google Document から自動生成されました*
"""
        
        # インデックスファイルを保存
        index_filepath = os.path.join(output_dir, f"{title}_インデックス.md")
        with open(index_filepath, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"📋 インデックスファイルを作成: {index_filepath}")
        print(f"\n🎉 {len(sections)}個のセクションを正常に分離しました！")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """メイン関数"""
    import sys
    
    # デフォルトのドキュメントURL
    default_url = "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing"
    
    document_url = sys.argv[1] if len(sys.argv) > 1 else default_url
    
    print("=== Google Document セクション分離ツール ===")
    print(f"対象URL: {document_url}")
    print()
    
    success = extract_sections_from_document(document_url)
    
    if success:
        print("\n🎉 セクション分離が正常に完了しました！")
    else:
        print("\n💥 セクション分離に失敗しました")
        sys.exit(1)

if __name__ == "__main__":
    main()
