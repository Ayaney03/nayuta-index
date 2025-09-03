# Google Document 同期システム

Google DocumentをCursor内のローカルMarkdownファイルに自動同期するシステムです。

## 🚀 クイックスタート

### 1. 初回セットアップ

```bash
# 依存関係をインストール
pip install -r requirements.txt

# Google Cloud Console で認証情報を取得し、credentials.json として保存
# 初回実行時にブラウザで認証が必要です
```

### 2. 単発同期

指定されたGoogle Documentを今すぐ同期：

```bash
# デフォルトドキュメント（瞑想YT_参考動画書き起こし）を同期
python sync_document.py

# 別のドキュメントを同期
python sync_document.py "https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit"
```

### 3. 複数ドキュメントの管理

```bash
# 登録されているドキュメント一覧を表示
python auto_sync_documents.py list

# 新しいドキュメントを追加
python auto_sync_documents.py add "ドキュメント名" "https://docs.google.com/document/d/..."

# すべてのドキュメントを一括同期
python auto_sync_documents.py sync
```

### 4. 自動同期（定期実行）

```bash
# 自動同期を開始（設定ファイルで間隔を指定）
python auto_sync_documents.py auto
```

## 📁 ファイル構成

```
google_drive_api/
├── google_drive_manager.py     # Google Drive API基本クラス
├── sync_document.py           # 単発同期スクリプト
├── auto_sync_documents.py     # 複数ドキュメント管理
├── sync_config.json          # 同期設定ファイル（自動生成）
├── requirements.txt          # 依存関係
├── credentials.json          # Google API認証情報（要設定）
└── token.pickle             # アクセストークン（自動生成）
```

## ⚙️ 設定ファイル（sync_config.json）

```json
{
  "documents": [
    {
      "name": "瞑想YT_参考動画書き起こし",
      "url": "https://docs.google.com/document/d/1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk/edit?usp=sharing",
      "output_dir": "../天郷事業/01_瞑想事業/瞑想YouTube",
      "enabled": true
    }
  ],
  "sync_interval_minutes": 30,
  "auto_sync": false
}
```

## 🎯 使用例

### 瞑想関連ドキュメントの同期

```bash
# 瞑想YT参考動画書き起こしを同期
python sync_document.py

# 結果: ../天郷事業/01_瞑想事業/瞑想YouTube/瞑想YT_参考動画書き起こし.md が作成される
```

### 新しいドキュメントを追加して同期

```bash
# 新しいドキュメントを登録
python auto_sync_documents.py add "新しい瞑想ガイド" "https://docs.google.com/document/d/NEW_DOC_ID/edit"

# 全ドキュメントを同期
python auto_sync_documents.py sync
```

### 自動同期の設定

1. `sync_config.json` で `auto_sync: true` に変更
2. `sync_interval_minutes` で同期間隔を設定（分単位）
3. 自動同期を開始：

```bash
python auto_sync_documents.py auto
```

## 📝 生成されるMarkdownファイルの形式

```markdown
# ドキュメントタイトル

> **同期元:** [Google Document](https://docs.google.com/...)  
> **最終同期:** 2024-01-15 14:30:00  
> **ドキュメントID:** 1R86x5NkHE6ETztRjntcLZ7seZGP_i1jv8uiAiYokcAk

---

（ドキュメントの内容）

---

*このファイルは Google Document から自動同期されています*
```

## 🔧 トラブルシューティング

### 認証エラー
- `credentials.json` が正しく配置されているか確認
- Google Cloud Console でAPI有効化を確認

### 権限エラー
- Google Documentの共有設定を確認
- 認証したアカウントにアクセス権があるか確認

### ファイルが見つからない
- ドキュメントURLが正しいか確認
- ドキュメントIDが正しく抽出されているか確認

## 🚀 Cursorでの活用方法

1. **コンテンツ作成の効率化**
   - Google Docsで下書き → 自動同期 → Cursorで編集・整形

2. **チーム協業**
   - 複数人でGoogle Docsで執筆 → 定期同期でローカル更新

3. **バージョン管理**
   - 同期されたMarkdownファイルをGitで管理
   - 変更履歴の追跡が可能

4. **AI活用**
   - 同期されたコンテンツに対してCursorのAI機能で指示
   - 「この内容を要約して」「この部分を詳しく説明して」など

## 💡 応用例

### 瞑想プログラム管理
```bash
# 瞑想関連ドキュメントをまとめて管理
python auto_sync_documents.py add "瞑想ガイド1" "https://docs.google.com/..."
python auto_sync_documents.py add "瞑想ガイド2" "https://docs.google.com/..."
python auto_sync_documents.py sync
```

### 定期レポート作成
- Google Docsで週次レポート作成
- 自動同期でCursorに取り込み
- AIで分析・要約・改善提案

これで、Google DocumentとCursorの間でシームレスな連携が可能になります！
