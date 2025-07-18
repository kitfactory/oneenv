# OneEnv Scaffolding API仕様書

## 概要

OneEnv Scaffolding機能の新API仕様。Scaffolding形式のテンプレートのみをサポートし、シンプルで直感的なAPIを提供。

## API関数一覧

### 1. get_all_template_structure()

**目的**: 全テンプレート構造をカテゴリ別オプション一覧で返却

```python
def get_all_template_structure() -> Dict[str, List[str]]:
    """
    インストールされた全パッケージからScaffolding形式テンプレートを収集し、
    カテゴリ別のオプション一覧を返却
    
    Returns:
        カテゴリ名をキー、オプション名のリストを値とする辞書
        
    Example:
        {
            "Database": ["sqlite", "postgres", "mysql"],
            "VectorStore": ["chroma", "weaviate", "pinecone"],
            "LLM": ["openai", "anthropic", "ollama"]
        }
    
    Raises:
        ImportError: entry-pointsの読み込みに失敗した場合
        ValueError: 不正なScaffolding形式テンプレートが見つかった場合
    """
```

**実装詳細:**
- entry-points 'oneenv.templates' から全テンプレート関数を発見
- 各テンプレート関数を実行してScaffolding形式データを取得
- `validate_scaffolding_format()` で形式検証
- 有効なテンプレートのみを処理、無効なものは警告ログ出力
- カテゴリ別にオプションをグループ化
- 重複オプションは除去

### 2. has_category()

**目的**: 指定カテゴリの存在確認

```python
def has_category(category: str) -> bool:
    """
    指定されたカテゴリが利用可能かどうかを確認
    
    Args:
        category: 確認するカテゴリ名（例: "Database", "VectorStore"）
        
    Returns:
        カテゴリが存在する場合True、存在しない場合False
        
    Example:
        >>> has_category("Database")
        True
        >>> has_category("NonExistent")
        False
    
    Raises:
        TypeError: categoryが文字列でない場合
        ValueError: categoryが空文字列の場合
    """
```

**実装詳細:**
- 引数の型・値チェック
- `get_all_template_structure()` を内部的に呼び出し
- 返された構造からカテゴリの存在を確認
- 大文字小文字を区別（厳密マッチ）

### 3. get_options()

**目的**: カテゴリ内の全オプション取得

```python
def get_options(category: str) -> List[str]:
    """
    指定されたカテゴリ内の全オプション名を取得
    
    Args:
        category: 対象カテゴリ名（例: "Database"）
        
    Returns:
        オプション名のリスト（カテゴリが存在しない場合は空リスト）
        
    Example:
        >>> get_options("Database")
        ["sqlite", "postgres", "mysql"]
        >>> get_options("NonExistent")
        []
    
    Raises:
        TypeError: categoryが文字列でない場合
        ValueError: categoryが空文字列の場合
    """
```

**実装詳細:**
- 引数の型・値チェック
- `get_all_template_structure()` を内部的に呼び出し
- 指定カテゴリのオプションリストを返却
- カテゴリが存在しない場合は空リストを返却（例外は発生させない）
- オプションはソート済みで返却

### 4. generate_template()

**目的**: 選択的テンプレート生成（利用側が直接指定）

```python
def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str:
    """
    指定された選択範囲に基づいて.envテンプレートファイルを生成
    
    Args:
        dest: 出力先ファイルパス（空文字列の場合はファイル出力なし）
        generation_range: 生成範囲指定のリスト
            [
                {"category": "Database", "option": "postgres"},     # 特定オプション
                {"category": "VectorStore", "option": "chroma"},    # 特定オプション  
                {"category": "LLM"}                                 # 全オプション
            ]
    
    Returns:
        生成された.envファイルの内容（文字列）
        
    Example:
        >>> content = generate_template("app.env", [
        ...     {"category": "Database", "option": "postgres"},
        ...     {"category": "LLM"}
        ... ])
        >>> print(content)
        # Database (postgres)
        DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
        DATABASE_POOL_SIZE=10
        
        # LLM (openai)
        OPENAI_API_KEY=
        OPENAI_MODEL=gpt-3.5-turbo
        
        # LLM (anthropic)
        ANTHROPIC_API_KEY=
        ANTHROPIC_MODEL=claude-3-sonnet
    
    Raises:
        TypeError: 引数の型が不正な場合
        ValueError: generation_rangeの形式が不正な場合
        FileNotFoundError: destの親ディレクトリが存在しない場合
        PermissionError: destファイルに書き込み権限がない場合
    """
```

**実装詳細:**
- 引数の型・値チェック
- generation_rangeの形式検証（必須キー: "category", オプショナルキー: "option"）
- 全テンプレートを読み込み、指定された選択範囲に一致する環境変数を抽出
- 環境変数をカテゴリ/オプション別にグループ化してコメント付きで出力
- destが指定されている場合はファイルに書き込み
- 生成された内容を文字列で返却

## 共通仕様

### エラーハンドリング

```python
class ScaffoldingError(Exception):
    """Scaffolding関連の基底例外"""
    pass

class TemplateFormatError(ScaffoldingError):
    """テンプレート形式エラー"""
    pass

class TemplateNotFoundError(ScaffoldingError):
    """テンプレートが見つからないエラー"""
    pass
```

### ログ出力

```python
import logging

logger = logging.getLogger('oneenv.scaffolding')

# 使用例
logger.warning(f"Skipping invalid template {entry_point.name}: {error}")
logger.info(f"Loaded {len(valid_templates)} valid templates")
logger.debug(f"Template structure: {structure}")
```

### キャッシュ戦略

```python
from functools import lru_cache
import hashlib
import json

@lru_cache(maxsize=1)
def _get_cached_template_structure() -> str:
    """
    テンプレート構造をキャッシュ（JSON文字列として）
    entry-pointsの変更検出のため、ハッシュ値もチェック
    """
    # パッケージリストのハッシュで変更検出
    package_hash = _get_packages_hash()
    structure = _load_template_structure_uncached()
    
    return json.dumps({
        "hash": package_hash,
        "structure": structure
    }, sort_keys=True)

def get_all_template_structure() -> Dict[str, List[str]]:
    """キャッシュを使用した構造取得"""
    cached_data = json.loads(_get_cached_template_structure())
    current_hash = _get_packages_hash()
    
    if cached_data["hash"] != current_hash:
        # キャッシュクリアして再読み込み
        _get_cached_template_structure.cache_clear()
        cached_data = json.loads(_get_cached_template_structure())
    
    return cached_data["structure"]
```

## テンプレート発見メカニズム

### entry-points設定

パッケージ開発者は以下の形式でテンプレート関数を登録：

```toml
# pyproject.toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
vectorstore = "mypackage.templates:vectorstore_template"
```

### テンプレート関数形式

```python
# mypackage/templates.py
def database_template():
    """
    データベース関連の環境変数テンプレート
    """
    return [
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL接続URL",
                    "default": "postgresql://user:pass@localhost:5432/dbname",
                    "required": True
                },
                "DATABASE_POOL_SIZE": {
                    "description": "コネクションプール最大サイズ",
                    "default": "10",
                    "required": False
                }
            }
        },
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLite接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        }
    ]
```

## .envファイル出力形式

### 基本フォーマット

```bash
# カテゴリ名 (オプション名)
VARIABLE_NAME=default_value
ANOTHER_VARIABLE=

# 次のカテゴリ
NEXT_CATEGORY_VAR=value
```

### 詳細仕様

```python
def generate_env_file_content(variables: Dict[str, Dict[str, Any]]) -> str:
    """
    環境変数辞書から.envファイル内容を生成
    
    Args:
        variables: {
            "var_name": {
                "value": "actual_value",
                "category": "Database", 
                "option": "postgres",
                "description": "変数の説明",
                "required": True
            }
        }
    """
    lines = []
    
    # カテゴリ/オプション別にグループ化
    grouped = {}
    for var_name, var_info in variables.items():
        category = var_info.get("category", "General")
        option = var_info.get("option", "default")
        key = f"{category} ({option})"
        
        if key not in grouped:
            grouped[key] = []
        grouped[key].append((var_name, var_info))
    
    # グループ別に出力
    for group_name, group_vars in grouped.items():
        lines.append(f"# {group_name}")
        
        for var_name, var_info in group_vars:
            # コメント行（説明）
            if var_info.get("description"):
                lines.append(f"# {var_info['description']}")
            
            # 変数行
            value = var_info.get("value", var_info.get("default", ""))
            lines.append(f"{var_name}={value}")
        
        lines.append("")  # 空行
    
    return "\n".join(lines)
```

## 使用例

### 基本的な使用パターン

```python
import oneenv

# 1. 利用可能な構成を確認
structure = oneenv.get_all_template_structure()
print("利用可能な構成:", structure)

# 2. 特定カテゴリの確認
if oneenv.has_category("Database"):
    options = oneenv.get_options("Database")
    print(f"Databaseオプション: {options}")

# 3. RAGアプリケーション用設定生成
content = oneenv.generate_template("rag_app.env", [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM"}  # 全LLMオプション
])

print("生成されたテンプレート:")
print(content)
```

### 利用側パッケージでの活用

```python
# ragapp/setup.py
import oneenv

def setup_rag_environment():
    """RAGアプリケーション環境のセットアップ"""
    
    # 必要なカテゴリが利用可能かチェック
    required_categories = ["Database", "VectorStore", "LLM"]
    missing = [cat for cat in required_categories if not oneenv.has_category(cat)]
    
    if missing:
        raise RuntimeError(f"Required categories not available: {missing}")
    
    # ユーザーに選択肢を提示
    print("利用可能なVectorStoreオプション:")
    for option in oneenv.get_options("VectorStore"):
        print(f"  - {option}")
    
    # デフォルト構成で生成
    oneenv.generate_template(".env.example", [
        {"category": "Database", "option": "postgres"},
        {"category": "VectorStore", "option": "chroma"},
        {"category": "LLM", "option": "openai"}
    ])
    
    print("✅ .env.exampleファイルを生成しました")
```

## パフォーマンス考慮

### 最適化手法

1. **LRUキャッシュ**: 構造情報の再計算を避ける
2. **遅延読み込み**: 必要な時のみテンプレート関数を実行
3. **バッチ処理**: entry-pointsの一括読み込み
4. **変更検出**: パッケージ変更時のみキャッシュクリア

## テスト要件

### 単体テスト

```python
def test_get_all_template_structure():
    """構造取得のテスト"""
    
def test_has_category():
    """カテゴリ存在確認のテスト"""
    
def test_get_options():
    """オプション取得のテスト"""
    
def test_generate_template():
    """テンプレート生成のテスト"""
    
def test_error_handling():
    """エラーハンドリングのテスト"""
```

### 統合テスト

```python
def test_end_to_end_workflow():
    """エンドツーエンドのワークフローテスト"""
    
def test_real_package_integration():
    """実際のパッケージとの統合テスト"""
```

## セキュリティ考慮

### 入力検証

- ファイルパス: パストラバーサル攻撃の防止
- テンプレートデータ: 任意コード実行の防止
- ユーザー入力: SQLインジェクション等の防止

### 権限管理

- ファイル作成権限の事前チェック
- 既存ファイル上書き時の確認
- テンプレート関数実行時の sandboxing (将来的検討)

## まとめ

この API仕様により：

1. **シンプル**: 4つの主要API関数のみ
2. **直感的**: category/optionベースの明確な構造
3. **柔軟**: 部分選択から全選択まで対応
4. **効率的**: キャッシュによる最適化
5. **安全**: 包括的なエラーハンドリング

利用側パッケージは簡単にOneEnvを活用してRAGスタック等の複雑な設定管理を実現できます。