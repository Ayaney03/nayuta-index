"""
Google Drive API Manager
スプレッドシート、ドキュメント、その他のファイルを取得するためのPythonクラス
"""

import os
import json
import pickle
from typing import List, Dict, Any, Optional
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
from io import BytesIO


class GoogleDriveManager:
    """Google Drive APIを使用してファイルを管理するクラス"""
    
    # 必要なスコープ（読み取り専用）
    SCOPES = [
        'https://www.googleapis.com/auth/drive.readonly',
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/documents.readonly'
    ]
    
    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.pickle'):
        """
        Google Drive Managerを初期化
        
        Args:
            credentials_file: OAuth2認証情報ファイルのパス
            token_file: アクセストークンを保存するファイルのパス
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.drive_service = None
        self.sheets_service = None
        self.docs_service = None
        
        # 認証を実行
        self._authenticate()
        
        # サービスを初期化
        self._initialize_services()
    
    def _authenticate(self):
        """Google APIの認証を行う"""
        # 既存のトークンファイルをチェック
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                self.creds = pickle.load(token)
        
        # 認証情報が無効または存在しない場合は再認証
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                # トークンをリフレッシュ
                self.creds.refresh(Request())
            else:
                # 新規認証
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"認証ファイル '{self.credentials_file}' が見つかりません。\n"
                        "Google Cloud Consoleから認証情報をダウンロードしてください。"
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            
            # トークンを保存
            with open(self.token_file, 'wb') as token:
                pickle.dump(self.creds, token)
    
    def _initialize_services(self):
        """APIサービスを初期化"""
        self.drive_service = build('drive', 'v3', credentials=self.creds)
        self.sheets_service = build('sheets', 'v4', credentials=self.creds)
        self.docs_service = build('docs', 'v1', credentials=self.creds)
    
    def list_files(self, query: str = None, max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Driveのファイル一覧を取得
        
        Args:
            query: 検索クエリ（例: "mimeType='application/vnd.google-apps.spreadsheet'"）
            max_results: 最大取得件数
            
        Returns:
            ファイル情報のリスト
        """
        try:
            results = self.drive_service.files().list(
                q=query,
                pageSize=max_results,
                fields="nextPageToken, files(id, name, mimeType, createdTime, modifiedTime, size, webViewLink)"
            ).execute()
            
            return results.get('files', [])
        
        except Exception as e:
            print(f"ファイル一覧取得エラー: {e}")
            return []
    
    def get_spreadsheet_data(self, spreadsheet_id: str, range_name: str = None) -> pd.DataFrame:
        """
        スプレッドシートのデータを取得してDataFrameとして返す
        
        Args:
            spreadsheet_id: スプレッドシートのID
            range_name: 取得範囲（例: 'Sheet1!A1:D10'）指定しない場合は全体を取得
            
        Returns:
            pandas DataFrame
        """
        try:
            if range_name is None:
                # シート一覧を取得して最初のシートの全体を取得
                spreadsheet = self.sheets_service.spreadsheets().get(
                    spreadsheetId=spreadsheet_id
                ).execute()
                
                sheet_name = spreadsheet['sheets'][0]['properties']['title']
                range_name = f"{sheet_name}"
            
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                return pd.DataFrame()
            
            # 最初の行をヘッダーとして使用
            df = pd.DataFrame(values[1:], columns=values[0])
            return df
        
        except Exception as e:
            print(f"スプレッドシート取得エラー: {e}")
            return pd.DataFrame()
    
    def get_document_content(self, document_id: str) -> Dict[str, Any]:
        """
        Googleドキュメントの内容を取得
        
        Args:
            document_id: ドキュメントのID
            
        Returns:
            ドキュメントの情報と内容を含む辞書
        """
        try:
            document = self.docs_service.documents().get(
                documentId=document_id
            ).execute()
            
            # テキスト内容を抽出
            content = ""
            for element in document.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    for text_run in element['paragraph'].get('elements', []):
                        if 'textRun' in text_run:
                            content += text_run['textRun'].get('content', '')
            
            return {
                'title': document.get('title', ''),
                'document_id': document_id,
                'content': content,
                'revision_id': document.get('revisionId', ''),
                'full_document': document
            }
        
        except Exception as e:
            print(f"ドキュメント取得エラー: {e}")
            return {}
    
    def search_files_by_name(self, name_pattern: str) -> List[Dict[str, Any]]:
        """
        ファイル名でファイルを検索
        
        Args:
            name_pattern: 検索パターン
            
        Returns:
            マッチしたファイルのリスト
        """
        query = f"name contains '{name_pattern}'"
        return self.list_files(query=query)
    
    def get_spreadsheets_list(self) -> List[Dict[str, Any]]:
        """スプレッドシートファイルのみを取得"""
        query = "mimeType='application/vnd.google-apps.spreadsheet'"
        return self.list_files(query=query)
    
    def get_documents_list(self) -> List[Dict[str, Any]]:
        """Googleドキュメントファイルのみを取得"""
        query = "mimeType='application/vnd.google-apps.document'"
        return self.list_files(query=query)
    
    def get_file_by_id(self, file_id: str) -> Dict[str, Any]:
        """
        ファイルIDから詳細情報を取得
        
        Args:
            file_id: ファイルのID
            
        Returns:
            ファイルの詳細情報
        """
        try:
            file_info = self.drive_service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, createdTime, modifiedTime, size, webViewLink, parents"
            ).execute()
            
            return file_info
        
        except Exception as e:
            print(f"ファイル詳細取得エラー: {e}")
            return {}
    
    def export_spreadsheet_as_csv(self, spreadsheet_id: str, sheet_name: str = None) -> str:
        """
        スプレッドシートをCSVとしてエクスポート
        
        Args:
            spreadsheet_id: スプレッドシートのID
            sheet_name: シート名（指定しない場合は最初のシート）
            
        Returns:
            CSV形式の文字列
        """
        try:
            # シート情報を取得
            if sheet_name is None:
                spreadsheet = self.sheets_service.spreadsheets().get(
                    spreadsheetId=spreadsheet_id
                ).execute()
                sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']
            else:
                # 指定されたシート名からシートIDを取得
                spreadsheet = self.sheets_service.spreadsheets().get(
                    spreadsheetId=spreadsheet_id
                ).execute()
                
                sheet_id = None
                for sheet in spreadsheet['sheets']:
                    if sheet['properties']['title'] == sheet_name:
                        sheet_id = sheet['properties']['sheetId']
                        break
                
                if sheet_id is None:
                    raise ValueError(f"シート '{sheet_name}' が見つかりません")
            
            # CSVとしてエクスポート
            export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"
            
            # 認証情報を使ってダウンロード
            import requests
            headers = {'Authorization': f'Bearer {self.creds.token}'}
            response = requests.get(export_url, headers=headers)
            
            if response.status_code == 200:
                return response.text
            else:
                raise Exception(f"エクスポートに失敗しました: {response.status_code}")
        
        except Exception as e:
            print(f"CSV エクスポートエラー: {e}")
            return ""


def extract_file_id_from_url(url: str) -> Optional[str]:
    """
    Google DriveのURLからファイルIDを抽出
    
    Args:
        url: Google DriveのURL
        
    Returns:
        ファイルID（見つからない場合はNone）
    """
    import re
    
    # スプレッドシートのURL形式
    spreadsheet_pattern = r'/spreadsheets/d/([a-zA-Z0-9-_]+)'
    # ドキュメントのURL形式
    document_pattern = r'/document/d/([a-zA-Z0-9-_]+)'
    # 一般的なファイルのURL形式
    file_pattern = r'/file/d/([a-zA-Z0-9-_]+)'
    
    for pattern in [spreadsheet_pattern, document_pattern, file_pattern]:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

