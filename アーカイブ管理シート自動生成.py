#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アーカイブ管理シート自動生成ツール
あやねえ専用 - ボタンひとつで秒速作成
"""

import os
from datetime import datetime
import json

class ArchiveSheetGenerator:
    def __init__(self):
        self.template = self._get_template()
    
    def _get_template(self):
        """アーカイブ管理シートのテンプレート構造"""
        return {
            "basic_info": {
                "title": "",
                "date": "",
                "speakers": "",
                "participants": "",
                "duration": "",
                "format": "",
                "location": ""
            },
            "overview": {
                "main_theme": "",
                "target_audience": [],
                "learning_objectives": []
            },
            "transcript_sections": [],
            "youtube_info": {
                "title_suggestions": [],
                "thumbnail_keywords": [],
                "description_template": ""
            },
            "quotes": [],
            "content_ideas": {
                "blog_articles": [],
                "line_distribution": [],
                "note_articles": [],
                "course_content": []
            },
            "checklist": {
                "transcript": [],
                "youtube_prep": [],
                "secondary_use": []
            },
            "memo": "",
            "related_files": []
        }
    
    def generate_sheet(self, **kwargs):
        """
        アーカイブ管理シートを生成
        
        Args:
            title: セミナータイトル
            date: 開催日時
            speakers: 講師名
            url: 録画URL
            duration: 録画時間
            main_theme: メインテーマ
            target_audience: 対象者（リスト）
            learning_objectives: 学習目標（リスト）
            **kwargs: その他のパラメータ
        """
        
        # 基本情報の設定
        basic_info = {
            "title": kwargs.get("title", ""),
            "date": kwargs.get("date", datetime.now().strftime("%Y年%m月%d日")),
            "speakers": kwargs.get("speakers", ""),
            "participants": kwargs.get("participants", ""),
            "duration": kwargs.get("duration", ""),
            "format": kwargs.get("format", "YouTube動画"),
            "location": kwargs.get("url", "")
        }
        
        # Markdownファイル生成
        content = self._generate_markdown(basic_info, **kwargs)
        
        # ファイル名生成
        safe_title = self._sanitize_filename(kwargs.get("title", "セミナー"))
        filename = f"{safe_title}_アーカイブ管理シート.md"
        
        # ファイル保存
        filepath = os.path.join("/Users/ayakamizuno/cursor", filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
    
    def _generate_markdown(self, basic_info, **kwargs):
        """Markdownコンテンツを生成"""
        
        content = f"""# セミナーアーカイブ管理シート

## 📝 基本情報

| 項目 | 内容 |
|------|------|
| セミナータイトル | {basic_info['title']} |
| 開催日時 | {basic_info['date']} |
| 講師 | {basic_info['speakers']} |
| 参加者数 | {basic_info['participants']} |
| 録画時間 | {basic_info['duration']} |
| ファイル形式 | {basic_info['format']} |
| 保存場所 | {basic_info['location']} |

---

## 🎯 セミナー概要

### メインテーマ
```
{kwargs.get('main_theme', 'メインテーマを記入してください')}
```

### 対象者
```
{self._format_list(kwargs.get('target_audience', ['対象者を記入してください']))}
```

### 学習目標
{self._format_objectives(kwargs.get('learning_objectives', ['学習目標を記入してください']))}

---

## 📋 文字起こし

### 導入部分（0:00-XX:XX）
```
・導入内容を記入
・重要ポイントを箇条書き
・印象的な発言
```

**重要なポイント：**
- ポイント1
- ポイント2
- ポイント3

### セクション2（XX:XX-XX:XX）
```
・セクション内容を記入
・重要ポイントを箇条書き
・具体的な事例
```

**重要なポイント：**
- ポイント1
- ポイント2
- ポイント3

---

## 🎬 YouTube活用情報

### 動画タイトル案
1. 【キーワード】メインタイトル
2. 【キーワード】サブタイトル
3. 【キーワード】別バージョン

### サムネイル用キーワード
- キーワード1
- キーワード2
- キーワード3
- キーワード4

### 概要欄テンプレート
```
🎥{basic_info['title']}

▶︎ この動画（音声）について
セミナーの概要説明をここに記入

✔︎ 学べること1
✔︎ 学べること2
✔︎ 学べること3

▶︎ この動画で学べること

✅ ポイント1の詳細説明
✅ ポイント2の詳細説明
✅ ポイント3の詳細説明

⏰ タイムスタンプ
00:00 導入
XX:XX セクション1
XX:XX セクション2
XX:XX まとめ

📚 関連リンク
・関連リンク1
・関連リンク2

💡 講師について
【{basic_info['speakers']}】
・プロフィール情報
・実績
・専門分野

🏷️ #ハッシュタグ1 #ハッシュタグ2 #ハッシュタグ3
```

---

## 💎 名言・印象的なフレーズ

### 引用可能な名言
1. "名言1をここに記入"
2. "名言2をここに記入"
3. "名言3をここに記入"

### SNS投稿用ショートクリップ候補
| 時間 | 内容 | 投稿文案 |
|------|------|----------|
| XX:XX-XX:XX | クリップ内容1 | 【キーワード】投稿文案1 |
| XX:XX-XX:XX | クリップ内容2 | 【キーワード】投稿文案2 |
| XX:XX-XX:XX | クリップ内容3 | 【キーワード】投稿文案3 |

---

## 📊 コンテンツ展開アイデア

### ブログ記事化
- [ ] 記事タイトル：タイトル案
- [ ] 構成案：構成の概要
- [ ] 公開予定日：日付

### LINE配信活用
- [ ] 配信タイトル：タイトル案
- [ ] 配信内容：内容の概要
- [ ] 配信予定日：日付

### note記事化
- [ ] noteタイトル：タイトル案
- [ ] 価格設定：価格
- [ ] 公開予定日：日付

### 講座コンテンツ化
- [ ] レッスンタイトル：タイトル案
- [ ] 対象講座：講座名
- [ ] 追加予定日：日付

---

## ✅ 作業チェックリスト

### 文字起こし作業
- [ ] 音声ファイルの準備
- [ ] AIツールでの一次起こし
- [ ] 手動での校正・編集
- [ ] 重要ポイントの抽出
- [ ] タイムスタンプの追加

### YouTube準備
- [ ] 動画編集
- [ ] サムネイル作成
- [ ] 概要欄作成
- [ ] タイトル決定
- [ ] 公開設定

### 二次活用
- [ ] ブログ記事作成
- [ ] SNS投稿準備
- [ ] LINE配信準備
- [ ] 講座コンテンツ化

---

## 📝 メモ・その他

```
・特記事項やメモをここに記入
・改善点や気づき
・次回への申し送り事項
```

---

## 🔗 関連ファイル・リンク

- 録画ファイル：{basic_info['location']}
- 資料ファイル：（追加予定）
- YouTube URL：（公開後追加）
- ブログ記事URL：（作成予定）
- 関連コンテンツ：（関連ファイル名）

---

## 📄 文字起こし原文

```
（文字起こし原文をここに貼り付け）
```
"""
        return content
    
    def _format_list(self, items):
        """リストを文字列形式に変換"""
        if isinstance(items, list):
            return '\n'.join([f"・{item}" for item in items])
        return str(items)
    
    def _format_objectives(self, objectives):
        """学習目標をMarkdown形式に変換"""
        if isinstance(objectives, list):
            return '\n'.join([f"- {obj}" for obj in objectives])
        return f"- {objectives}"
    
    def _sanitize_filename(self, filename):
        """ファイル名を安全な形式に変換"""
        # 使用できない文字を置換
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 長すぎる場合は短縮
        if len(filename) > 50:
            filename = filename[:50]
        
        return filename

def main():
    """メイン実行関数"""
    generator = ArchiveSheetGenerator()
    
    # サンプル実行
    sample_data = {
        "title": "サンプルセミナー",
        "date": "2025年1月15日",
        "speakers": "あやねえ",
        "participants": "20名",
        "duration": "約60分",
        "url": "https://example.com/video",
        "main_theme": "AIを活用した効率的なワークフロー構築術",
        "target_audience": [
            "AI活用に興味があるビジネスパーソン",
            "効率化を求める起業家・フリーランス",
            "クライアントワークで収入を上げたい人"
        ],
        "learning_objectives": [
            "AIツールの実践的な活用方法を学ぶ",
            "ワークフローの効率化手法を身につける",
            "クライアントワークでの成果向上を実現する"
        ]
    }
    
    filepath = generator.generate_sheet(**sample_data)
    print(f"アーカイブ管理シートを生成しました: {filepath}")

if __name__ == "__main__":
    main()

