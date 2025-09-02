#!/usr/bin/env python3
"""
脱スマホ瞑想プログラム専用同期システム
天郷事業の瞑想プログラムをGoogle Driveに同期し、チームアクセスを可能にする
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path
from google_drive_manager import GoogleDriveManager

class MeditationProgramSync:
    def __init__(self):
        self.google_drive_path = "/Users/ayakamizuno/Library/CloudStorage/GoogleDrive-hamuchu@gmail.com/マイドライブ"
        self.drive_manager = GoogleDriveManager()
        
        # 脱スマホ瞑想プログラム設定
        self.program_config = {
            "name": "脱スマホ瞑想プログラム",
            "local_path": "/Users/ayakamizuno/cursor/天郷事業/01_瞑想事業/脱スマホ瞑想プログラム",
            "sync_folder": "脱スマホ瞑想プログラム_チーム共有",
            "team_type": "なゆたさん・制作チーム",
            "html_folder": "HTMLページ_Web公開用"
        }
        
        # 同期対象外のファイル・フォルダ
        self.exclude_patterns = [
            '.DS_Store',
            '.git',
            '__pycache__',
            '*.pyc',
            'Icon',
            '.gitignore',
            'node_modules',
            '~'  # 一時フォルダを除外
        ]
    
    def should_exclude(self, file_path):
        """ファイル・フォルダが同期対象外かどうかを判定"""
        file_name = os.path.basename(file_path)
        
        for pattern in self.exclude_patterns:
            if pattern.startswith('*'):
                if file_name.endswith(pattern[1:]):
                    return True
            else:
                if file_name == pattern:
                    return True
        return False
    
    def copy_with_exclusions(self, src, dst):
        """除外パターンを考慮してファイル・フォルダをコピー"""
        if os.path.exists(dst):
            shutil.rmtree(dst)
        
        os.makedirs(dst, exist_ok=True)
        
        copied_files = []
        skipped_files = []
        html_files = []
        
        for root, dirs, files in os.walk(src):
            # 除外対象のディレクトリを削除
            dirs[:] = [d for d in dirs if not self.should_exclude(os.path.join(root, d))]
            
            # 相対パスを計算
            rel_root = os.path.relpath(root, src)
            dst_root = os.path.join(dst, rel_root) if rel_root != '.' else dst
            
            # ディレクトリを作成
            os.makedirs(dst_root, exist_ok=True)
            
            # ファイルをコピー
            for file in files:
                src_file = os.path.join(root, file)
                
                if self.should_exclude(src_file):
                    skipped_files.append(src_file)
                    continue
                
                dst_file = os.path.join(dst_root, file)
                try:
                    shutil.copy2(src_file, dst_file)
                    copied_files.append(dst_file)
                    
                    # HTMLファイルを記録
                    if file.endswith('.html'):
                        html_files.append({
                            'name': file,
                            'path': dst_file,
                            'relative_path': os.path.relpath(dst_file, dst)
                        })
                        
                except Exception as e:
                    print(f"ファイルコピーエラー: {src_file} -> {dst_file}: {e}")
        
        return copied_files, skipped_files, html_files
    
    def create_html_access_page(self, sync_target_path, html_files):
        """HTMLファイルアクセス用のインデックスページを作成"""
        html_folder = os.path.join(sync_target_path, self.program_config["html_folder"])
        os.makedirs(html_folder, exist_ok=True)
        
        # HTMLファイルをHTMLフォルダにもコピー
        for html_info in html_files:
            src_html = html_info['path']
            dst_html = os.path.join(html_folder, html_info['name'])
            shutil.copy2(src_html, dst_html)
        
        # インデックスページを作成
        index_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>脱スマホ瞑想プログラム - HTMLページ一覧</title>
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Yu Gothic', sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.2em;
        }}
        .update-info {{
            background: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 5px;
        }}
        .html-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .html-card {{
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            background: #f9f9f9;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .html-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .html-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }}
        .html-link {{
            display: inline-block;
            background: #007bff;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.2s;
        }}
        .html-link:hover {{
            background: #0056b3;
        }}
        .instructions {{
            background: #e7f3ff;
            border: 1px solid #b3d9ff;
            border-radius: 10px;
            padding: 20px;
            margin-top: 30px;
        }}
        .instructions h3 {{
            color: #0066cc;
            margin-top: 0;
        }}
        .access-note {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧘‍♀️ 脱スマホ瞑想プログラム</h1>
        <h2>📱 HTMLページ一覧</h2>
        
        <div class="update-info">
            <strong>📅 最終更新:</strong> {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}<br>
            <strong>👤 更新者:</strong> あやねえ<br>
            <strong>📁 総ファイル数:</strong> {len(html_files)}個のHTMLページ
        </div>
        
        <div class="access-note">
            <strong>🔗 アクセス方法:</strong><br>
            各HTMLページをクリックすると、新しいタブで開きます。<br>
            Google Driveで直接HTMLを表示するため、レイアウトが崩れる場合があります。<br>
            正確な表示を確認したい場合は、ファイルをダウンロードしてブラウザで開いてください。
        </div>
        
        <div class="html-grid">"""
        
        for html_info in html_files:
            # Google DriveでHTMLファイルを開くためのリンクを生成
            # 実際のファイルパスからGoogle Drive URLを生成する必要があります
            file_name = html_info['name']
            
            index_content += f"""
            <div class="html-card">
                <div class="html-title">📄 {file_name}</div>
                <p>瞑想プログラムのコンテンツページです</p>
                <a href="{file_name}" class="html-link" target="_blank">
                    📖 ページを開く
                </a>
            </div>"""
        
        index_content += f"""
        </div>
        
        <div class="instructions">
            <h3>📋 利用方法</h3>
            <ol>
                <li><strong>ページ閲覧:</strong> 上記のリンクをクリックして各ページを確認</li>
                <li><strong>ダウンロード:</strong> 必要に応じてファイルを右クリック→ダウンロード</li>
                <li><strong>編集依頼:</strong> 修正が必要な箇所があればあやねえまで連絡</li>
                <li><strong>最新版確認:</strong> このページを再読み込みして最新の更新情報を確認</li>
            </ol>
            
            <h3>👥 対象メンバー</h3>
            <p>{self.program_config["team_type"]}</p>
            
            <h3>📞 連絡先</h3>
            <p>質問や修正依頼は、あやねえまでお気軽にご連絡ください。</p>
        </div>
    </div>
</body>
</html>"""
        
        index_path = os.path.join(html_folder, "index.html")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        return index_path, html_folder
    
    def create_team_notification(self, sync_target_path, html_files):
        """チーム向けの通知ファイルを作成"""
        notification_file = os.path.join(sync_target_path, "📢_最新更新情報.md")
        
        content = f"""# 📢 {self.program_config['name']} 最新更新情報

## 🕐 最終更新日時
{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

## 👤 更新者
あやねえ

## 📝 更新内容
Cursorで編集した脱スマホ瞑想プログラムのコンテンツを最新版に同期しました。

## 👥 対象
{self.program_config['team_type']}の皆様

## 📁 主要な更新箇所
- 各フォルダの最新コンテンツを確認してください
- HTMLページ: {len(html_files)}個のページが利用可能
- 新規追加ファイルがある場合は特に注意してください

## 🌐 HTMLページアクセス方法
1. 「{self.program_config['html_folder']}」フォルダを開く
2. 「index.html」をクリックしてページ一覧を表示
3. 各HTMLページをクリックして内容を確認

## 📱 HTMLページ一覧
"""
        
        for html_info in html_files:
            content += f"- 📄 {html_info['name']}\n"
        
        content += f"""
## 🔄 次回同期予定
手動実行またはあやねえからの指示により更新

## 📞 連絡事項
- 新しいコンテンツを確認してください
- HTMLページの表示に問題がある場合は連絡してください
- 質問や修正が必要な箇所があれば連絡してください
- 必要に応じて作業を進めてください

## 💡 ヒント
- HTMLページはGoogle Driveで直接表示されますが、正確な表示確認にはダウンロードを推奨
- モバイルでも閲覧可能ですが、PCでの閲覧を推奨

---
**このファイルは自動生成されます**
"""
        
        try:
            with open(notification_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"📢 通知ファイルを作成: {notification_file}")
        except Exception as e:
            print(f"❌ 通知ファイル作成エラー: {e}")
    
    def sync_meditation_program(self):
        """脱スマホ瞑想プログラムを同期"""
        local_path = self.program_config["local_path"]
        sync_folder = self.program_config["sync_folder"]
        sync_target_path = os.path.join(self.google_drive_path, sync_folder)
        
        print(f"🔄 {self.program_config['name']}を同期中...")
        
        if not os.path.exists(local_path):
            print(f"❌ ローカルフォルダが見つかりません: {local_path}")
            return False
        
        try:
            # Google Driveフォルダにコピー
            print(f"📁 コピー先: {sync_target_path}")
            copied_files, skipped_files, html_files = self.copy_with_exclusions(local_path, sync_target_path)
            
            # HTMLアクセスページを作成
            if html_files:
                print(f"🌐 HTMLページを処理中... ({len(html_files)}個)")
                index_path, html_folder = self.create_html_access_page(sync_target_path, html_files)
                print(f"📖 HTMLインデックスページを作成: {index_path}")
            
            # 同期ログを作成
            sync_log = {
                "project": self.program_config['name'],
                "sync_time": datetime.now().isoformat(),
                "source_path": local_path,
                "target_path": sync_target_path,
                "copied_files_count": len(copied_files),
                "skipped_files_count": len(skipped_files),
                "html_files_count": len(html_files),
                "html_files": [html['name'] for html in html_files],
                "status": "success"
            }
            
            # ログファイルを保存
            log_path = os.path.join(sync_target_path, "sync_log.json")
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(sync_log, f, ensure_ascii=False, indent=2)
            
            # 通知ファイルを作成
            self.create_team_notification(sync_target_path, html_files)
            
            print(f"✅ {self.program_config['name']} 同期完了!")
            print(f"   📄 コピーしたファイル: {len(copied_files)}件")
            print(f"   🌐 HTMLページ: {len(html_files)}件")
            print(f"   ⏭️  スキップしたファイル: {len(skipped_files)}件")
            print(f"   📍 同期先: {sync_target_path}")
            
            if html_files:
                print(f"   📖 HTMLアクセス: {html_folder}/index.html")
            
            return True
            
        except Exception as e:
            print(f"❌ {self.program_config['name']} 同期エラー: {e}")
            return False

def main():
    """メイン実行関数"""
    sync = MeditationProgramSync()
    
    print("🧘‍♀️ 脱スマホ瞑想プログラム同期システム")
    print("=" * 60)
    
    # 同期実行
    success = sync.sync_meditation_program()
    
    if success:
        print("\n📋 次のステップ:")
        print("1. Google Driveで同期されたフォルダを確認")
        print("   📁 フォルダ名: 脱スマホ瞑想プログラム_チーム共有")
        print("2. HTMLページフォルダでindex.htmlを開いてページ一覧を確認")
        print("3. なゆたさん・チームメンバーに共有リンクを送信")
        print("4. 必要に応じて編集権限を設定")
        
        print("\n🔗 共有設定の手順:")
        print("1. Google Driveで「脱スマホ瞑想プログラム_チーム共有」フォルダを右クリック")
        print("2. 「共有」を選択")
        print("3. 「リンクを知っている全員」に設定")
        print("4. 「閲覧者」または「編集者」権限を選択")
        print("5. 生成されたリンクをチームに送信")
    else:
        print("\n❌ 同期に失敗しました。エラーを確認してください。")

if __name__ == "__main__":
    main()
