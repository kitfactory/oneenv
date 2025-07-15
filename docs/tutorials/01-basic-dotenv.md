# Step 1: 基本的なdotenv使用法

**所要時間:** 5-10分  
**難易度:** 初級

## 学習目標

- 環境変数の基本概念を理解する
- `.env` ファイルの作成と使用方法を学ぶ
- OneEnvを使った基本的な環境変数の読み込みを実践する

## 従来の問題点

### 1. ハードコーディングの問題

```python
# 悪い例: 設定がハードコーディング
def connect_to_database():
    host = "localhost"
    port = 5432
    database = "myapp"
    username = "admin"
    password = "secret123"
    # 本番環境では異なる設定が必要...
```

### 2. OS環境変数の問題

```python
import os

# 設定が散在、管理が困難
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/myapp")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

## OneEnvによる解決策

### ステップ1: OneEnvをインストール

```bash
pip install oneenv
```

### ステップ2: .envファイルを作成

プロジェクトのルートディレクトリに `.env` ファイルを作成：

```bash
# .env
DATABASE_URL=postgresql://localhost:5432/myapp
SECRET_KEY=your-secret-key-here
DEBUG=True
API_KEY=your-api-key
LOG_LEVEL=INFO
```

### ステップ3: OneEnvを使って読み込み

```python
# app.py
import oneenv
import os

# 環境変数を読み込み
oneenv.load_dotenv()

# 設定を取得
database_url = os.getenv("DATABASE_URL")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG", "False").lower() == "true"

print(f"Database URL: {database_url}")
print(f"Debug mode: {debug}")
```

## 実践演習

### 演習1: 基本的な設定管理

1. 新しいディレクトリを作成してください：
```bash
mkdir oneenv-tutorial
cd oneenv-tutorial
```

2. `.env` ファイルを作成：
```bash
APP_NAME=My Tutorial App
PORT=8000
DATABASE_URL=sqlite:///tutorial.db
SECRET_KEY=tutorial-secret-key
DEBUG=True
```

3. Pythonスクリプトを作成（`basic_config.py`）：
```python
import oneenv
import os

# 環境変数を読み込み
oneenv.load_dotenv()

# 設定を表示
print("=== アプリケーション設定 ===")
print(f"アプリ名: {os.getenv('APP_NAME')}")
print(f"ポート: {os.getenv('PORT')}")
print(f"データベース: {os.getenv('DATABASE_URL')}")
print(f"デバッグモード: {os.getenv('DEBUG')}")
```

4. 実行：
```bash
python basic_config.py
```

### 演習2: デフォルト値の設定

設定にデフォルト値を追加してみましょう：

```python
# config_with_defaults.py
import oneenv
import os

oneenv.load_dotenv()

# デフォルト値付きで設定を取得
app_name = os.getenv("APP_NAME", "Default App")
port = int(os.getenv("PORT", "3000"))
debug = os.getenv("DEBUG", "False").lower() == "true"
log_level = os.getenv("LOG_LEVEL", "INFO")

print("=== 設定（デフォルト値付き） ===")
print(f"アプリ名: {app_name}")
print(f"ポート: {port}")
print(f"デバッグ: {debug}")
print(f"ログレベル: {log_level}")
```

### 演習3: 辞書として設定を取得

```python
# config_as_dict.py
import oneenv

# 設定を辞書として取得
config = oneenv.dotenv_values()

print("=== 全設定 ===")
for key, value in config.items():
    print(f"{key}: {value}")
```

## OneEnvの利点

### 1. 簡潔性
```python
# 従来の方法
from dotenv import load_dotenv
load_dotenv()

# OneEnvの方法
import oneenv
oneenv.load_dotenv()
```

### 2. 型安全性
OneEnvは将来的に型安全性を提供します（Pydanticサポート）。

### 3. 拡張性
次のステップで学ぶテンプレート自動生成機能への準備ができます。

## 次のステップ

基本的なdotenvの使用方法を学びました。次は、OneEnvの強力な機能である自動テンプレート生成を学びましょう。

**→ [Step 2: OneEnvによる自動テンプレート生成](02-template-generation.md)**

## 参考資料

- [python-dotenv documentation](https://github.com/theskumar/python-dotenv)
- [12-Factor App: Config](https://12factor.net/config)
- [OneEnv メインドキュメント](../../README_ja.md)

## よくある質問

### Q: .envファイルはGitにコミットすべきですか？
A: いいえ。`.env`ファイルには機密情報が含まれるため、`.gitignore`に追加してください。代わりに`.env.example`をコミットします。

### Q: 環境変数が読み込まれない場合は？
A: `.env`ファイルがPythonスクリプトと同じディレクトリにあることを確認してください。異なる場所にある場合は、`oneenv.load_dotenv("path/to/.env")`のようにパスを指定できます。