# 顧客情報管理システム

このフォルダには、無明会のメンバー（顧客）情報を管理するためのファイルが含まれています。

## ファイル構成

### HTMLファイル（データベース画面）
- `メンバーデータベース.html` - メインのメンバーデータベース（完全版）
- `メンバーデータベース_改良版.html` - CSV読み込み機能付きの改良版
- `メンバーデータベース_シンプル版.html` - シンプルな表示版
- `member_detail.html` - 個別メンバー詳細表示画面

### データファイル
- `members_data.csv` - メンバーの基本データ（CSV形式）

### JavaScriptマッピングファイル
- `annual_payment_dates_mapping.js` - 年間決済日マッピング
- `current_member_status_mapping.js` - 現在のメンバーステータス
- `discord_mapping.js` - Discordアカウント情報
- `member_furigana_mapping.js` - メンバー名のふりがな
- `regular_join_dates_mapping.js` - 正規入会日
- `three_poisons_team_mapping.js` - 三毒チーム分け
- `trial_dates_mapping.js` - 体験期間データ

## 使用方法

1. **メインデータベース**: `メンバーデータベース.html`を開いて、メンバー情報の一覧表示・検索・フィルタリングが可能
2. **CSV読み込み**: `メンバーデータベース_改良版.html`でCSVファイルを読み込んで動的にデータを更新
3. **個別詳細**: `member_detail.html`で特定メンバーの詳細情報を表示

## 注意事項

- 顧客の個人情報が含まれているため、取り扱いには十分注意してください
- ファイルの編集・更新時は必ずバックアップを取ってから行ってください
