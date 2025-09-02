# Google Drive同期設定手順

## 🎯 目標
CursorワークスペースをGoogle Driveと同期し、Notionでチーム共有できるようにする

## 📋 実装手順

### Step 1: Google Drive for Desktop セットアップ
1. **ダウンロード・インストール**
   - [Google Drive for Desktop](https://www.google.com/drive/download/) からダウンロード
   - インストール後、あやねえのGoogleアカウントでサインイン

2. **同期設定**
   - 同期フォルダ: `/Users/ayakamizuno/Google Drive/`
   - 「マイドライブをこのデバイスに同期」を有効化

### Step 2: ワークスペース移動
```bash
# 現在のワークスペースをGoogle Driveにコピー
cp -r "/Users/ayakamizuno/cursor/秘書力マスター講座" "/Users/ayakamizuno/Google Drive/秘書力マスター講座"

# Cursorで新しい場所を開く
code "/Users/ayakamizuno/Google Drive/秘書力マスター講座"
```

### Step 3: Notion連携設定
1. **チーム共有Notionページ作成**
   - プロジェクト管理用のメインページ
   - タスク管理データベース
   - ファイル管理セクション

2. **Google Drive埋め込み**
   ```
   /google → Google Driveファイルを選択
   ```

3. **チームメンバー招待**
   - Google Drive: 編集権限で共有
   - Notion: 適切な権限レベルで招待

## 🔄 同期の仕組み

```
Cursor編集 → Google Drive自動同期 → Notion埋め込み更新 → チーム確認
```

## 📊 管理構造案

### Notionページ構成
```
📋 秘書力マスター講座 プロジェクト
├── 📁 レッスンコンテンツ (Google Drive同期)
│   ├── 第1章〜第9章フォルダ
│   └── 資料リンク集
├── 📋 タスク管理
│   ├── あやねえタスク
│   ├── ゆうこさんタスク
│   └── チーム共通タスク
├── 📅 制作スケジュール
└── 📊 進捗レポート
```

## ✅ 完了チェックリスト
- [ ] Google Drive for Desktop インストール
- [ ] ワークスペース移動・同期確認
- [ ] Notionページ作成
- [ ] Google Drive埋め込み設定
- [ ] チームメンバー招待
- [ ] 同期テスト実行

---
*作成日: 2025年1月27日*
*担当: あやねえ + チーム*
