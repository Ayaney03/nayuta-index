# 秘書力マスター講座 Google Drive チーム共有手順書

## 🎯 概要
秘書力マスター講座のプロジェクトフォルダをGoogle Driveでチーム共有し、効率的な協業環境を構築します。

## 📋 事前準備

### 必要なもの
- [ ] Google アカウント（あやねえ）
- [ ] チームメンバーのメールアドレス
- [ ] Google Cloud Console プロジェクト
- [ ] OAuth 2.0 認証情報

### Google Cloud Console設定
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成：「秘書力マスター講座-チーム共有」
3. 以下のAPIを有効化：
   - Google Drive API
   - Google Sheets API
   - Google Docs API

4. OAuth 2.0 認証情報を作成：
   - 「APIとサービス」→「認証情報」
   - 「認証情報を作成」→「OAuth クライアント ID」
   - アプリケーションの種類：「デスクトップアプリケーション」
   - ダウンロードしたJSONファイルを `credentials.json` として保存

## 🚀 アップロード手順

### Step 1: 環境準備
```bash
cd /Users/ayakamizuno/cursor/google_drive_api

# 必要なライブラリをインストール
pip install -r requirements.txt

# 認証ファイルを配置
# credentials.json を google_drive_api フォルダに配置
```

### Step 2: フォルダアップロード実行
```bash
# アップロードスクリプトを実行
python folder_uploader.py
```

**初回実行時の流れ：**
1. ブラウザが自動で開く
2. Googleアカウントでログイン
3. アクセス許可を承認
4. アップロード開始

### Step 3: アップロード結果確認
アップロード完了後、以下の情報が `drive_upload_result.json` に保存されます：
```json
{
  "folder_id": "Google DriveフォルダID",
  "share_link": "共有リンクURL",
  "upload_date": "2025-01-27",
  "folder_name": "秘書力マスター講座"
}
```

## 👥 チーム共有設定

### 方法1: メールアドレスで直接共有
`folder_uploader.py` の `team_emails` リストにメンバーのメールアドレスを追加：

```python
team_emails = [
    "yukosan@example.com",
    "team_member2@example.com"
]
```

### 方法2: 共有リンクを使用
1. アップロード完了後に表示される共有リンクをコピー
2. チームメンバーにリンクを送信
3. 必要に応じて権限レベルを調整

### 権限レベル
- **閲覧者（reader）**: ファイルの表示のみ
- **編集者（writer）**: ファイルの編集・追加・削除可能
- **オーナー（owner）**: 完全な管理権限

## 📁 フォルダ構造（Google Drive上）

```
📁 秘書力マスター講座/
├── 📁 チーム運営/
│   ├── 📄 Cursor活用ワークフロー.md
│   ├── 📄 Google_Drive同期設定手順.md
│   └── 📁 MTG議事録/
├── 📁 マーケティング/
│   ├── 📁 LINE配信/
│   ├── 📁 SNS投稿/
│   └── 📁 ローンチ計画/
├── 📁 レッスン（講座コンテンツ）/
│   ├── 📄 レッスン構造一覧.md
│   ├── 📁 第1章_講座の使い方ガイダンス/
│   ├── 📁 第2章_稼げるオンライン秘書のマインド/
│   └── ... (第9章まで)
└── 📄 資料リンク集.md
```

## 🔄 同期とワークフロー

### 推奨ワークフロー
1. **ローカル編集**: Cursorで通常通り編集
2. **Google Drive同期**: 定期的にアップロードスクリプトを実行
3. **チーム確認**: Google Drive上でチームメンバーが確認・コメント
4. **フィードバック反映**: ローカルで修正後、再度同期

### 自動同期設定（オプション）
Google Drive for Desktop を使用した自動同期も可能：

```bash
# ワークスペースをGoogle Driveフォルダに移動
mv "/Users/ayakamizuno/cursor/秘書力マスター講座" "/Users/ayakamizuno/Google Drive/"

# Cursorで新しい場所を開く
code "/Users/ayakamizuno/Google Drive/秘書力マスター講座"
```

## 🛡️ セキュリティとベストプラクティス

### セキュリティ対策
- [ ] `credentials.json` をGitリポジトリにコミットしない
- [ ] チームメンバーの権限を適切に設定
- [ ] 定期的にアクセス権限を見直し
- [ ] 機密情報を含むファイルは別途管理

### ファイル管理ルール
- [ ] ファイル名は日本語OK、スペースは避ける
- [ ] バージョン管理が必要なファイルは命名規則を統一
- [ ] 削除前は必ずチームに確認
- [ ] 大きなファイル（動画等）は圧縮してアップロード

## 📊 Notion連携

### Google Drive埋め込み手順
1. Notionページで `/google` と入力
2. 共有したいGoogle Driveファイル/フォルダを選択
3. 埋め込み設定を調整

### 推奨Notion構成
```
📋 秘書力マスター講座 プロジェクト管理
├── 🎯 プロジェクト概要
├── 📁 Google Drive フォルダ (埋め込み)
├── 📋 タスク管理データベース
├── 📅 制作スケジュール
├── 👥 チームメンバー
└── 📊 進捗レポート
```

## ❓ トラブルシューティング

### よくある問題と解決方法

**Q: 認証エラーが発生する**
A: `credentials.json` が正しく配置されているか確認。Google Cloud ConsoleでAPIが有効化されているか確認。

**Q: アップロードが途中で止まる**
A: ネットワーク接続を確認。大きなファイルがある場合は時間がかかる場合があります。

**Q: チームメンバーがアクセスできない**
A: 共有設定を確認。メールアドレスが正確か、権限レベルが適切か確認。

**Q: ファイルが重複している**
A: 既存のフォルダを削除してから再アップロード、または手動で重複ファイルを削除。

## 📞 サポート

### 連絡先
- **技術的な問題**: あやねえ
- **アクセス権限の問題**: プロジェクト管理者
- **Notion連携**: チーム運営担当

### 参考資料
- [Google Drive API ドキュメント](https://developers.google.com/drive/api)
- [Notion Google Drive 連携ガイド](https://www.notion.so/help/google-drive-integration)

---
**作成日**: 2025年1月27日  
**更新日**: 2025年1月27日  
**担当者**: あやねえ  
**バージョン**: 1.0
