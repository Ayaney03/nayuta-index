#!/bin/bash
# Google Drive for Desktop 自動同期スクリプト

echo "🚀 Google Drive自動同期開始..."

# ファイルパス定義
SOURCE_FILE="/Users/ayakamizuno/cursor/天郷事業/01_瞑想事業/脱スマホ瞑想プログラム_商品提案.html"
DRIVE_FILE="$HOME/Library/CloudStorage/GoogleDrive-hamuchu@gmail.com/My Drive/脱スマホ瞑想プログラム_商品提案.html"

# 1. 更新日を現在時刻に更新
CURRENT_TIME=$(date '+%Y年%m月%d日 %H:%M')
echo "📅 更新日を更新: $CURRENT_TIME"

# HTMLファイル内の更新日を置換
sed -i '' "s/📅 最終更新: [0-9]\{4\}年[0-9]\{2\}月[0-9]\{2\}日 [0-9]\{2\}:[0-9]\{2\}/📅 最終更新: $CURRENT_TIME/g" "$SOURCE_FILE"

if [ $? -eq 0 ]; then
    echo "✅ 更新日の更新完了"
else
    echo "❌ 更新日の更新に失敗"
    exit 1
fi

# 2. Google Driveフォルダにコピー
echo "📂 Google Driveに同期中..."

# Google Driveフォルダの存在確認
if [ ! -d "$HOME/Library/CloudStorage/GoogleDrive-hamuchu@gmail.com/My Drive/" ]; then
    echo "❌ Google Drive for Desktopフォルダが見つかりません"
    echo "   Google Drive for Desktopがインストール・ログインされているか確認してください"
    exit 1
fi

# ファイルをコピー
cp "$SOURCE_FILE" "$DRIVE_FILE"

if [ $? -eq 0 ]; then
    echo "✅ Google Driveへのコピー完了"
else
    echo "❌ Google Driveへのコピーに失敗"
    exit 1
fi

# 3. 完了メッセージ
echo ""
echo "🎉 同期完了！"
echo "📁 ファイル場所: My Drive/脱スマホ瞑想プログラム_商品提案.html"
echo "🔗 数分後に https://drive.google.com で確認できます"
echo ""

# 4. 共有手順のリマインダー
echo "📋 なゆたさんへの共有手順:"
echo "1. https://drive.google.com を開く"
echo "2. '脱スマホ瞑想プログラム_商品提案.html' を右クリック"
echo "3. '共有' → 'リンクを知っている全員が閲覧可' → 'リンクをコピー'"
echo "4. なゆたさんにリンクを送信"
echo ""

# 5. 共有メッセージのテンプレート
echo "💌 なゆたさんへの送信メッセージ例:"
echo "────────────────────────────────────"
echo "なゆたさん、お疲れさまです！"
echo ""
echo "脱スマホ瞑想プログラムの提案ページを更新しました✨"
echo "以下のリンクからご確認ください："
echo ""
echo "📄 提案ページ: [ここにコピーしたリンクを貼り付け]"
echo ""
echo "【見方】"
echo "1. 上のリンクをタップ"
echo "2. 「ダウンロード」ボタンを押す"
echo "3. ダウンロードしたファイルをタップして開く"
echo ""
echo "💡 今後の更新も同じリンクで最新版が見られます！"
echo "   ページ右下の更新日で最新かどうか確認できます📅"
echo "   最終更新: $CURRENT_TIME"
echo ""
echo "何かご質問があれば、いつでもお声がけくださいね！"
echo ""
echo "あやねえ"
echo "────────────────────────────────────"
