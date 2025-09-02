# Google Driveでの脱スマホ瞑想プログラム提案ページ共有手順

## 📁 方法1：手動アップロード（推奨・最も簡単）

### 手順
1. **Google Driveにアクセス**
   - ブラウザで [drive.google.com](https://drive.google.com) を開く

2. **ファイルをアップロード**
   - 「新規」ボタン → 「ファイルのアップロード」をクリック
   - `脱スマホ瞑想プログラム_商品提案.html` を選択してアップロード

3. **共有設定**
   - アップロードしたファイルを右クリック → 「共有」を選択
   - 「リンクを知っている全員が閲覧可」に設定
   - 「リンクをコピー」でURLを取得

4. **なゆたさんに送信**
   - コピーしたリンクをなゆたさんに送信
   - なゆたさんはブラウザでHTMLファイルをダウンロード後、開いて閲覧可能

---

## 🤖 方法2：API経由での自動アップロード

### 前提条件
- Google Drive API認証が設定済み
- `google_drive_api` フォルダ内のツールが利用可能

### 手順

#### 1. 認証確認
```bash
cd /Users/ayakamizuno/cursor/google_drive_api
python -c "from google_drive_manager import GoogleDriveManager; gdm = GoogleDriveManager(); print('認証成功')"
```

#### 2. ファイルアップロード用スクリプト実行
```python
# upload_html_file.py として保存・実行
from google_drive_manager import GoogleDriveManager
from googleapiclient.http import MediaFileUpload
import os

def upload_html_to_drive(file_path, file_name):
    """HTMLファイルをGoogle Driveにアップロード"""
    
    # Google Drive Managerを初期化
    gdm = GoogleDriveManager()
    
    # ファイルメタデータ
    file_metadata = {
        'name': file_name,
        'parents': []  # 特定フォルダに入れたい場合はフォルダIDを指定
    }
    
    # ファイルをアップロード
    media = MediaFileUpload(file_path, mimetype='text/html')
    
    file = gdm.drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink, webContentLink'
    ).execute()
    
    # 共有設定（リンクを知っている全員が閲覧可能）
    gdm.drive_service.permissions().create(
        fileId=file.get('id'),
        body={
            'role': 'reader',
            'type': 'anyone'
        }
    ).execute()
    
    return {
        'file_id': file.get('id'),
        'view_link': file.get('webViewLink'),
        'download_link': file.get('webContentLink')
    }

# 実行
file_path = '/Users/ayakamizuno/cursor/天郷事業/01_瞑想事業/脱スマホ瞑想プログラム_商品提案.html'
file_name = '脱スマホ瞑想プログラム_商品提案.html'

result = upload_html_to_drive(file_path, file_name)
print(f"アップロード完了！")
print(f"閲覧用リンク: {result['view_link']}")
print(f"ダウンロード用リンク: {result['download_link']}")
```

---

## 📱 方法3：GitHub Pages経由での公開（上級者向け）

### 手順
1. **GitHubリポジトリ作成**
   - 新しいパブリックリポジトリを作成

2. **ファイルアップロード**
   - `index.html` として提案ページをアップロード

3. **GitHub Pages有効化**
   - Settings → Pages → Source: Deploy from a branch
   - Branch: main → Save

4. **公開URLを取得**
   - `https://[ユーザー名].github.io/[リポジトリ名]/` でアクセス可能

---

## 🎯 推奨方法

**方法1（手動アップロード）** が最も簡単で確実です。

### なゆたさんへの共有メッセージ例

```
なゆたさん、お疲れさまです！

脱スマホ瞑想プログラムの商品提案ページを作成しました。
以下のリンクからご確認ください：

📄 提案ページ: [Google Driveリンク]

【閲覧方法】
1. 上記リンクをクリック
2. 「ダウンロード」ボタンでHTMLファイルをダウンロード
3. ダウンロードしたファイルをブラウザで開いて閲覧

ご質問やご要望がございましたら、いつでもお声がけください！

あやねえ
```

---

## 🔧 トラブルシューティング

### HTMLファイルが正しく表示されない場合
- ファイルを右クリック → 「プログラムから開く」→ ブラウザを選択
- または、ブラウザを開いてファイルをドラッグ&ドロップ

### 共有リンクが機能しない場合
- 共有設定を「リンクを知っている全員」に変更
- ファイルの権限設定を確認

### API認証エラーの場合
- `token.pickle` ファイルを削除して再認証
- `credentials.json` ファイルが正しい場所にあるか確認
