よ？#!/bin/bash
# 脱スマホ瞑想プログラムHTMLファイル自動同期スクリプト

echo "🚀 脱スマホ瞑想プログラム Google Drive自動同期開始..."

# 現在の日時を取得
CURRENT_TIME=$(date '+%Y年%m月%d日 %H:%M')
echo "📅 更新日を更新: $CURRENT_TIME"

# 同期するHTMLファイルのリスト
FILES=(
    "なゆたセミナー台本_脱スマホ瞑想プログラム.html"
    "脱スマホ瞑想プログラム_全章台本.html"
    "00_脱スマホ瞑想プログラム_ハブ.html"
    "LINE_bot構想_いつでも瞑想見守るくん.html"
)

# 各ファイルをGoogle Driveフォルダにコピー
for file in "${FILES[@]}"; do
    if [ -f "/Users/ayakamizuno/cursor/天郷事業/01_瞑想事業/脱スマホ瞑想プログラム/$file" ]; then
        echo "📂 $file を同期中..."
        cp "/Users/ayakamizuno/cursor/天郷事業/01_瞑想事業/脱スマホ瞑想プログラム/$file" \
           "~/Library/CloudStorage/GoogleDrive-hamuchu@gmail.com/My Drive/脱スマホ瞑想プログラム/$file"
    else
        echo "⚠️  $file が見つかりません"
    fi
done

echo "✅ 同期完了！Google Drive for Desktopが自動でクラウドにアップロードします"
echo "🔗 数分後にhttps://drive.google.com で確認できます"

# 共有リンク生成のヒント表示
echo ""
echo "📋 那由多さんへの共有手順:"
echo "1. https://drive.google.com を開く"
echo "2. '脱スマホ瞑想プログラム' フォルダを開く"
echo "3. 共有したいファイルを右クリック"
echo "4. '共有' → 'リンクを知っている全員が閲覧可' → 'リンクをコピー'"
echo "5. 那由多さんにリンクを送信"

echo ""
echo "🌟 那由多さんへの共有メッセージ例:"
echo "---"
echo "那由多さん、お疲れさまです！"
echo ""
echo "脱スマホ瞑想プログラムの資料を更新しました✨"
echo "以下のリンクからご確認ください："
echo ""
echo "📄 資料: [ここにコピーしたリンクを貼り付け]"
echo ""
echo "【見方】"
echo "1. 上のリンクをタップ"
echo "2. 「ダウンロード」ボタンを押す"
echo "3. ダウンロードしたファイルをタップして開く"
echo ""
echo "何かご質問があれば、いつでもお声がけくださいね！"
echo ""
echo "あやねえ"
echo "---"
