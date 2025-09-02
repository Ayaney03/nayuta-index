# Notion ↔ Cursor 双方向同期システム 完全ガイド

## 🎯 概要
チームメンバーがNotionでドキュメントを編集すると、自動的にCursorのローカルファイルにも反映される双方向同期システムです。

## ✨ 主な機能

### 🔄 双方向同期
- **Cursor → Notion**: ローカルファイル編集時に自動でNotionに反映
- **Notion → Cursor**: Notionでの編集を定期的にローカルに反映
- **リアルタイム同期**: Webhook使用時は即座に反映

### ⚠️ 競合解決
- **自動検出**: 同時編集による競合を自動検出
- **解決方法**: 対話的選択、自動解決、手動マージ
- **バックアップ**: 競合時に自動でバックアップを作成

### 📊 監視・管理
- **ファイル監視**: リアルタイムでローカルファイル変更を検出
- **同期ログ**: 全ての同期操作を記録
- **Web管理画面**: ブラウザで同期状況を確認

## 🚀 セットアップ手順

### Step 1: 環境準備
```bash
cd /Users/ayakamizuno/cursor/google_drive_api

# 必要なライブラリをインストール
pip install -r requirements.txt

# セットアップスクリプトを実行
python setup_notion_sync.py
```

### Step 2: Notion Integration 作成
1. [Notion Integrations](https://www.notion.so/my-integrations) にアクセス
2. **"New integration"** をクリック
3. 設定項目を入力：
   ```
   名前: 秘書力マスター講座同期
   ワークスペース: あやねえのワークスペース
   機能: Read content, Update content, Insert content
   ```
4. **"Submit"** をクリック
5. **"Internal Integration Token"** をコピー

### Step 3: ページ接続設定
同期したい各Notionページで：
1. ページ右上の **"..."** メニューをクリック
2. **"接続"** → **"秘書力マスター講座同期"** を選択
3. **"確認"** をクリック

### Step 4: ファイルマッピング
セットアップスクリプトで以下を設定：
- ローカルファイルとNotionページのリンク
- 同期対象ファイルの選択
- 競合解決方法の設定

## 📋 使用方法

### 基本的な同期
```bash
# 同期システムを開始
./start_notion_sync.sh

# 同期システムを停止
./stop_notion_sync.sh
```

### 手動同期
```bash
# 特定ファイルをNotionに同期
curl -X POST "http://localhost:8080/sync/manual/レッスン構造一覧.md?direction=local_to_notion"

# Notionからローカルに同期
curl -X POST "http://localhost:8080/sync/manual/レッスン構造一覧.md?direction=notion_to_local"

# 双方向同期
curl -X POST "http://localhost:8080/sync/manual/レッスン構造一覧.md?direction=both"
```

### 同期状況確認
```bash
# ブラウザで管理画面を開く
open http://localhost:8080/sync/status

# コマンドラインで確認
curl http://localhost:8080/sync/status
```

## 🔧 詳細設定

### 同期設定ファイル
`.notion_sync_config.json` で以下を設定可能：

```json
{
  "page_mappings": {
    "レッスン構造一覧.md": "notion_page_id_here"
  },
  "sync_enabled": true,
  "auto_sync_interval": 30,
  "conflict_resolution": "manual"
}
```

### 競合解決戦略
```json
{
  "conflict_resolution": "manual",     // 対話的に選択
  "conflict_resolution": "local_wins", // ローカル優先
  "conflict_resolution": "notion_wins" // Notion優先
}
```

### 環境変数設定
`.env` ファイルで設定：
```bash
NOTION_TOKEN=your_notion_integration_token
NOTION_WEBHOOK_SECRET=your_webhook_secret  # オプション
WEBHOOK_PORT=8080                          # オプション
```

## 🌐 Webhook設定（推奨）

### ngrok を使用した外部公開
```bash
# ngrokをインストール
brew install ngrok

# ローカルサーバーを外部公開
ngrok http 8080
```

### Notion Webhook 設定
1. [Notion Developers](https://developers.notion.com/) にアクセス
2. Integration を選択
3. **"Webhooks"** タブを開く
4. **"Add webhook"** をクリック
5. 設定：
   ```
   URL: https://your-ngrok-url.ngrok.io/webhook/notion
   Events: page.updated, block.updated
   ```

## 📁 ファイル構造

```
google_drive_api/
├── notion_sync_manager.py      # メイン同期システム
├── notion_webhook_server.py    # Webhookサーバー
├── conflict_resolver.py        # 競合解決システム
├── setup_notion_sync.py        # セットアップスクリプト
├── requirements.txt            # 必要ライブラリ
├── start_notion_sync.sh        # 開始スクリプト
├── stop_notion_sync.sh         # 停止スクリプト
└── .env                        # 環境変数（要作成）

秘書力マスター講座/
├── .notion_sync_config.json    # 同期設定
├── .notion_conflicts.json      # 競合ログ
└── .notion_backups/            # バックアップフォルダ
    ├── レッスン構造一覧_local_20250127_143022.md
    └── notion_content_20250127_143022.md
```

## 🔄 ワークフロー例

### 日常的な使用
1. **朝**: `./start_notion_sync.sh` で同期開始
2. **作業中**: 
   - Cursorでファイル編集 → 自動でNotionに同期
   - チームメンバーがNotionで編集 → 自動でCursorに同期
3. **夕方**: `./stop_notion_sync.sh` で同期停止

### チーム協業
1. **あやねえ**: Cursorでレッスン内容を作成・編集
2. **チームメンバー**: Notionで内容確認・コメント・修正
3. **システム**: 変更を自動で双方向同期
4. **競合時**: 自動検出 → 解決方法を選択 → バックアップ作成

## ⚠️ 競合解決の流れ

### 競合検出時
```
⚠️ 編集競合が検出されました: レッスン構造一覧.md
============================================================

📊 変更差分:
--- ローカルファイル
+++ Notion
@@ -1,3 +1,3 @@
 # レッスン構造一覧
 
-## 第1章: 基礎編
+## 第1章: 基礎編（更新版）

🔧 競合解決方法を選択してください:
1. ローカルファイルを優先（Notionを上書き）
2. Notionを優先（ローカルファイルを上書き）
3. 手動でマージ（エディタで編集）
4. スキップ（後で手動解決）

選択してください (1-4):
```

### 手動マージ時
```
📝 マージファイルを作成しました: .notion_backups/merge_20250127_143022.md

## ⚠️ 編集競合が発生しました
以下の内容を確認して、最終的な内容を作成してください。

## 📝 ローカルファイルの内容:
# レッスン構造一覧
## 第1章: 基礎編

## 🌐 Notionの内容:
# レッスン構造一覧
## 第1章: 基礎編（更新版）

## ✅ 最終的な内容（以下に記入）:
# レッスン構造一覧
## 第1章: 基礎編（チーム更新版）
```

## 📊 監視・ログ

### 同期ログの確認
```bash
# 競合履歴を表示
python conflict_resolver.py

# 同期設定を確認
cat .notion_sync_config.json

# バックアップ一覧
ls -la .notion_backups/
```

### Web管理画面
ブラウザで `http://localhost:8080` にアクセス：
- 同期状況の確認
- 手動同期の実行
- 競合履歴の表示
- システムヘルスチェック

## 🛡️ セキュリティとベストプラクティス

### セキュリティ対策
- [ ] `.env` ファイルをGitリポジトリにコミットしない
- [ ] Notion Integration Token を適切に管理
- [ ] Webhook Secret を設定（本番環境）
- [ ] 定期的にアクセス権限を見直し

### ファイル管理
- [ ] 重要なファイルは事前にバックアップ
- [ ] 大きなファイルは同期対象から除外
- [ ] バイナリファイルは同期しない
- [ ] 定期的に古いバックアップを削除

### チーム運用ルール
- [ ] 同時編集時は事前にチームに連絡
- [ ] 重要な変更前はバックアップを作成
- [ ] 競合発生時は速やかに解決
- [ ] 定期的に同期状況を確認

## ❓ トラブルシューティング

### よくある問題

**Q: 同期が動作しない**
```
A: 確認事項
1. NOTION_TOKEN が正しく設定されているか
2. Notionページに Integration が接続されているか
3. ファイルマッピングが正しく設定されているか
4. 同期システムが起動しているか
```

**Q: 競合が頻繁に発生する**
```
A: 対策
1. チーム内で編集スケジュールを調整
2. 自動解決戦略を設定
3. より頻繁な同期間隔に設定
4. セクション別にファイルを分割
```

**Q: Webhookが動作しない**
```
A: 確認事項
1. ngrok が正しく動作しているか
2. Webhook URL が正しく設定されているか
3. ファイアウォールの設定
4. Notion側のWebhook設定
```

## 📞 サポート

### 連絡先
- **技術的な問題**: あやねえ
- **Notion設定**: プロジェクト管理者
- **チーム運用**: チーム運営担当

### 参考資料
- [Notion API ドキュメント](https://developers.notion.com/)
- [Flask ドキュメント](https://flask.palletsprojects.com/)
- [Watchdog ドキュメント](https://python-watchdog.readthedocs.io/)

---
**作成日**: 2025年1月27日  
**更新日**: 2025年1月27日  
**担当者**: あやねえ  
**バージョン**: 1.0
