# Google Drive API連携マニュアル - 実作業ログ

## 実際のやり取りログ

### 最初の要望（ユーザーの質問）

> Googleドライブからスプレッドシート、ドキュメントなどの情報を引っ張っていきたい。 API経由がいいです。

### セットアップ開始時のやり取り

**ユーザー**: セットアップお願いします。

**作業開始**: Google Drive APIのセットアップを実行

#### 最初のつまずきポイント - pipがない問題

**実行したコマンド**:
```bash
cd /Users/ayakamizuno/cursor/google_drive_api && pip install -r requirements.txt
```

**エラー結果**:
```
ayakamizuno@cd /Users/ayakamizuno/cursor/google_drive_api && pip install -r requirements.txt install -r requ
zsh: command not found: pip
```

**ユーザーの反応**: アイルは入ってるのに、どうしたらいいの？

**解決方法**: Python3を使用
```bash
python3 --version && which python3
# → Python 3.9.6 /usr/bin/python3 確認

python3 -m pip install -r requirements.txt
```

**成功結果**: 
- ライブラリインストール完了
- 警告メッセージ: `WARNING: You are using pip version 21.2.4; however, version 25.2 is available.`
- urllib3の警告: `NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+`

### テスト実行時のやり取り

**ユーザー**: テストお願い

**最初のテスト実行**:
```bash
python3 example_usage.py
```

**結果**: 認証URLが表示されて処理が止まる
```
=== Google Drive API Manager デモ ===

1. Google Drive APIに接続中...
Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=134367404602-i3a92s1p8rovlh7ao6hmi3a3h81evtcm.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A55214%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets.readonly+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments.readonly&state=VlWfVtQyXtRZCX2q8NtsYyJJ0V6pzd&access_type=offline
```

**問題**: 初回認証でブラウザ認証が必要だが、中断された

**ユーザー**: もっかいテスト

**対処**: シンプルなテストスクリプト `simple_test.py` を作成

**2回目のテスト実行**:
```bash
python3 simple_test.py
```

**認証完了**: ブラウザで認証後、`token.pickle` ファイルが自動生成される

### 認証完了後の成功

**テスト結果**: 正常動作を確認
```
=== Google Drive API 接続テスト ===

✓ credentials.json 確認完了
Google Drive APIに接続中...
Please visit this URL to authorize this application: [認証URL表示]

✓ Google Drive API接続成功

ファイル一覧を取得中（最初の5件）...
✓ 5件のファイルを取得成功

取得したファイル:
  1. NEW ★つぐみさんインスタ投稿内容★ (application/vnd.google-apps.spreadsheet)
  2. Google OAuth 審査プロセス (application/vnd.google-makersuite.prompt)
  3. image.png (image/png)
  4. ChromeでMacが重い (application/vnd.google-makersuite.prompt)
  5. image.png (image/png)

スプレッドシート一覧を取得中...
✓ スプレッドシート 100件を発見
Googleドキュメント一覧を取得中...
✓ Googleドキュメント 100件を発見

=== 接続テスト完了 ===
Google Drive APIが正常に動作しています！

=== LINE関連ファイル検索テスト ===

「LINE」を検索中...
  → 100件発見
    1. 2508ローンチLINE配信設定テンプレ
    2. LINE配信250819-0831公式_ブラッシュアップ版.csv
    3. LINE配信250819-0831公式_ブラッシュアップ版.csv
「恋愛note」を検索中...
  → 3件発見
「配信」を検索中...
  → 13件発見

=== 検索テスト完了 ===
```

### 写真取得の追加要望

**ユーザー**: Google DriveのAPIでフィリピンに住んでた時の写真のフォルダを持ってきて。

**作業**: philippines_photo_finder.py を作成・実行

**実行中断**: 処理が長時間かかって中断

**ユーザー**: どこに保存してる？

**確認**: `/Users/ayakamizuno/cursor/フィリピン写真` に保存済みを確認

### マニュアル作成の要望

**ユーザー**: この手順を、秘書業務のフォルダの中にまとめておいてほしい

**ユーザー**: このチャットで話した内容をそのままマークダウンでまとめておいてほしいです。いずれ自分で人に説明してAPIの設定などをできる人を増やすためです。

**最終要望**: このチャットの最初から話した内容をそのままなんかログとして残したいです。最初どんな風に聞いて、例えばこのチャットだったら、スプレッドシートやドキュメントやドライブを引っ張ってこれるようにしたいです、みたいな聞き方したと思うんですけど、そのラフな聞き方したやつをそのまんまで、私が質問した内容はそのまんまで、このチャット内でやったAPIの連携の手続きをまとめて、マニュアルというか、人に説明できるようにするために残しておいてほしいです。

## 実施した作業の全手順

### 1. 初期セットアップ

#### 1-1. 必要なPythonライブラリの準備

作成したファイル: `requirements.txt`
```txt
google-api-python-client==2.110.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.1.0
google-auth==2.25.2
pandas==2.1.4
openpyxl==3.1.2
python-docx==1.1.0
```

#### 1-2. メインのAPI管理クラスの作成

作成したファイル: `google_drive_manager.py`

**主な機能:**
- Google Drive APIの認証管理
- スプレッドシートの取得（pandas DataFrameとして）
- Googleドキュメントの取得（テキスト形式）
- ファイル検索機能
- CSVエクスポート機能
- URLからファイルIDを抽出する機能

#### 1-3. 使用例とデモコードの作成

作成したファイル: `example_usage.py`
- 基本的な使用方法のデモンストレーション
- ファイル一覧取得の例
- スプレッドシート・ドキュメント取得の例

#### 1-4. LINE配信ファイル専用プロセッサーの作成

作成したファイル: `line_distribution_processor.py`
- LINE配信関連ファイルの自動検索
- スプレッドシート → CSV形式で保存
- ドキュメント → マークダウン形式で保存
- `無明会/2508恋愛noteローンチ（5期）/LINE` フォルダに自動保存

#### 1-5. セットアップスクリプトの作成

作成したファイル: `setup_and_run.py`
- ライブラリの自動インストール
- 認証ファイルの確認
- 実行オプションの選択機能

### 2. Google Cloud Console設定手順

#### 2-1. プロジェクト作成とAPI有効化

1. **Google Cloud Console**にアクセス: https://console.cloud.google.com/
2. **新しいプロジェクトを作成**または既存のプロジェクトを選択
3. **以下のAPIを有効化**:
   - Google Drive API
   - Google Sheets API
   - Google Docs API

#### 2-2. OAuth認証情報の作成

1. Google Cloud Consoleで「**APIとサービス**」→「**認証情報**」を選択
2. 「**認証情報を作成**」→「**OAuth クライアント ID**」を選択
3. アプリケーションの種類で「**デスクトップアプリケーション**」を選択
4. 名前を入力（例：「あやねえGoogle Drive API」）
5. 「**作成**」をクリック

#### 2-3. 認証ファイルのダウンロードと配置

1. 作成された認証情報の**ダウンロードボタン**をクリック
2. JSONファイルをダウンロード
3. ダウンロードしたファイルを `credentials.json` という名前に変更
4. `/Users/ayakamizuno/cursor/google_drive_api/` フォルダに保存

### 3. 実際のセットアップ実行

#### 3-1. ライブラリのインストール

実行したコマンド:
```bash
cd /Users/ayakamizuno/cursor/google_drive_api
python3 -m pip install -r requirements.txt
```

**結果**: 必要なライブラリが正常にインストール完了

#### 3-2. 認証ファイルの配置確認

認証ファイル `credentials.json` をプロジェクトフォルダに配置

### 4. 動作テスト

#### 4-1. 基本接続テスト

作成したテストファイル: `simple_test.py`

実行したコマンド:
```bash
python3 simple_test.py
```

**テスト結果:**
- ✅ Google Drive API接続: 成功
- ✅ 認証: 完了（初回実行時にブラウザで認証）
- ✅ ファイル一覧取得: 5件取得成功
- ✅ スプレッドシート検索: 100件発見
- ✅ Googleドキュメント検索: 100件発見
- ✅ LINE関連ファイル検索: 
  - 「LINE」: 100件発見
  - 「恋愛note」: 3件発見
  - 「配信」: 13件発見

#### 4-2. LINE配信ファイルの実際の取得テスト

実行したコマンド:
```bash
python3 line_distribution_processor.py
```

**取得結果:**
- 総ファイル数: 105件発見
- 処理成功: 6件
- 取得できたファイル:
  1. 2508ローンチLINE配信設定テンプレ.csv (14行)
  2. LINE配信叩きテンプレコピー用雛形.csv (95行)
  3. LINE配信文.md (153文字)
  4. あやねえさんLINE運用引き継ぎ.md (593文字)
  5. 📢【マニュアル作成例】LINE公式あいさつメッセージ追加対応.md (963文字)
  6. 無明会マーケ_2506恋愛note.md (1627文字)

**保存先**: `/Users/ayakamizuno/cursor/無明会/2508恋愛noteローンチ（5期）/LINE/`

### 5. 写真取得機能の追加

#### 5-1. ユーザーの追加要望

> Google DriveのAPIでフィリピンに住んでた時の写真のフォルダを持ってきて。

#### 5-2. 写真取得専用スクリプトの作成

作成したファイル: `philippines_photo_finder.py`

**機能:**
- フィリピン関連キーワードでの検索（フィリピン、セブ、マニラ等）
- フォルダ内の画像ファイル自動検出
- 画像ファイルの自動ダウンロード
- フォルダ構造を保持した整理保存
- 写真一覧インデックスの自動生成

#### 5-3. 写真取得の実行

実行したコマンド:
```bash
python3 philippines_photo_finder.py
```

**取得結果:**
- 総ファイル数: 32件発見
- フォルダ数: 13件
- 画像ファイル数: 約49枚取得成功

**保存先**: `/Users/ayakamizuno/cursor/フィリピン写真/`

**取得された写真フォルダ:**
- 2304-フィリピン/
- 2402🇵🇭セブ合宿/
  - 240216-18ヴィラ/ (5枚)
  - 240217マリバゴグリル/ (10枚)
  - 240218-ホテル・ルーフトップ/ (10枚)
  - 240218ナイトマーケット/ (3枚)
  - 240219マゼランクロス・教会/ (10枚)
  - 240220おまけ/ (10枚)

## 最終的に作成されたファイル構成

```
google_drive_api/
├── requirements.txt                   # 必要なPythonライブラリ
├── google_drive_manager.py           # メインのAPIマネージャークラス
├── example_usage.py                  # 使用例とデモコード
├── line_distribution_processor.py    # LINE配信ファイル専用プロセッサー
├── philippines_photo_finder.py       # 写真取得専用スクリプト
├── simple_test.py                    # 基本動作テスト用
├── setup_and_run.py                 # セットアップとクイックスタート
├── README.md                         # 詳細な使用方法と説明
├── credentials.json                  # OAuth認証情報（要作成）
└── token.pickle                      # アクセストークン（自動生成）
```

## 使用可能になった機能

### 1. スプレッドシート取得
```python
from google_drive_manager import GoogleDriveManager

drive_manager = GoogleDriveManager()
df = drive_manager.get_spreadsheet_data("スプレッドシートID")
```

### 2. Googleドキュメント取得
```python
doc_content = drive_manager.get_document_content("ドキュメントID")
print(doc_content['content'])
```

### 3. ファイル検索
```python
files = drive_manager.search_files_by_name("検索キーワード")
```

### 4. LINE配信ファイル自動取得
```bash
python3 line_distribution_processor.py
```

### 5. 写真フォルダ取得（サンプル：フィリピン写真）
```bash
python3 philippines_photo_finder.py
```

## トラブルシューティング

### よくあるエラー
1. **認証エラー**: `credentials.json` ファイルが正しく配置されているか確認
2. **スコープエラー**: APIが有効化されているか確認
3. **権限エラー**: ファイルに適切なアクセス権限があるか確認

### 注意事項
- 初回実行時にブラウザで認証画面が表示される
- `credentials.json` ファイルは機密情報のため、Gitリポジトリにコミットしない
- APIの使用制限に注意（無料枠あり）
- 大量のファイルを処理する場合は適切な間隔を設ける

## 今後の拡張可能性

1. **他の写真フォルダ対応**: キーワードを変更することで任意の写真フォルダを取得可能
2. **自動同期機能**: 定期実行によるファイルの自動同期
3. **ファイル形式の拡張**: PDF、Excel等の他形式ファイルの取得
4. **フォルダ構造の保持**: Google Drive上のフォルダ構造をローカルに完全再現
5. **差分更新**: 変更されたファイルのみを取得する機能

## まとめ

このマニュアルに従うことで、Google Drive APIを使用したファイル取得システムを構築できます。スプレッドシート、ドキュメント、写真など様々なファイル形式に対応し、自動化された取得・整理機能を提供します。
