# OneEnv Scaffolding System Data Models Design

## 概要

OneEnvスキャフォールディング機能のための新しいデータモデル設計書。既存の `EnvTemplate` システムと共存し、カテゴリ/オプション基盤のインタラクティブ環境変数選択を可能にします。

## 新データモデル設計

### 1. EnvOption Model

**目的**: カテゴリ内の単一オプション（例：VectorStore内のChroma）を表現

```python
class EnvOption(BaseModel):
    """
    カテゴリ内の選択可能オプションを表現
    例: VectorStoreカテゴリ内のChromaオプション
    """
    category: str = Field(
        ...,
        min_length=1,
        description="カテゴリ名（例：Database, VectorStore, RAG）"
    )
    option: str = Field(
        ...,
        min_length=1,
        description="オプション名（例：sqlite, chroma, openai）"
    )
    env: Dict[str, EnvVarConfig] = Field(
        ...,
        description="このオプション選択時に有効になる環境変数設定"
    )
    description: Optional[str] = Field(
        default="",
        description="このオプションの説明"
    )
    dependencies: Optional[List[str]] = Field(
        default_factory=list,
        description="依存する他のカテゴリ/オプション（例：['vectorstore:chroma']）"
    )
    tags: Optional[List[str]] = Field(
        default_factory=list,
        description="検索・フィルタリング用タグ"
    )
    priority: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="表示優先度（1=高優先度, 1000=低優先度）"
    )
```

**設計ポイント**:
- `category` + `option` で一意のオプションを識別
- `env` は既存の `EnvVarConfig` を再利用
- `dependencies` で他オプションとの依存関係を表現
- `priority` で表示順序を制御

### 2. 簡素化された設計アプローチ

利用側パッケージが選択判断を行うため、OneEnvは以下の2つの機能に特化：

1. **情報提供**: どのようなカテゴリ・オプションが利用可能かを提供
2. **生成実行**: 指定されたカテゴリ・オプションでテンプレートファイルを生成

**冗長な中間モデルを除去:**
- `ScaffoldingTemplate` - 削除（パッケージ側で管理）
- `ScaffoldingChoice` - 削除（利用側で判断）

### 2. スキャフォールディング情報構造

**新形式テンプレート関数（パッケージ側）:**

```python
# mypackage/templates.py
def database_template():
    """
    スキャフォールディング対応の新形式
    """
    return [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLiteデータベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        },
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
        }
    ]
```

### 3. 直接的なAPI設計

利用側パッケージが直接使用するシンプルなAPI：

```python
# 1. 情報取得API
structure = oneenv.get_all_template_structure()
# 戻り値: {
#   "Database": ["sqlite", "postgres", "mysql"],
#   "VectorStore": ["chroma", "weaviate"], 
#   "LLM": ["openai", "anthropic", "ollama"]
# }

# カテゴリ存在確認
has_db = oneenv.has_category("Database")  # True/False

# オプション一覧取得
db_options = oneenv.get_options("Database")  # ["sqlite", "postgres", "mysql"]

# 2. 生成API（利用側が直接指定）
oneenv.generate_template("app.env", [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM"}  # option未指定=全オプション
])
```

## 既存システムとの互換性

### 既存EnvTemplateとの共存

**戦略**: 新旧システムを並行稼働させ、段階的移行を支援

```python
class CompatibilityLayer:
    """
    既存EnvTemplateと新ScaffoldingTemplateの互換性レイヤー
    """
    
    @staticmethod
    def convert_legacy_to_scaffolding(env_template: EnvTemplate) -> ScaffoldingTemplate:
        """
        既存EnvTemplateを新ScaffoldingTemplate形式に変換
        """
        # groupでグループ化されたアイテムをcategory/optionに変換
        
    @staticmethod
    def convert_scaffolding_to_legacy(scaffolding_template: ScaffoldingTemplate) -> EnvTemplate:
        """
        新ScaffoldingTemplateを既存EnvTemplate形式に変換
        """
        # category/optionをgroupに統合
```

### 形式判別メカニズム

```python
def detect_template_format(template_data: Dict[str, Any]) -> Literal["legacy", "groups", "scaffolding"]:
    """
    テンプレートデータの形式を自動判別
    """
    if isinstance(template_data, list) and all(
        isinstance(item, dict) and 
        "category" in item and 
        "option" in item and 
        "env" in item 
        for item in template_data
    ):
        return "scaffolding"
    elif "groups" in template_data:
        return "groups"
    else:
        return "legacy"
```

## シンプルなAPI設計

### 1. get_all_template_structure()

```python
def get_all_template_structure() -> Dict[str, List[str]]:
    """
    全テンプレート構造をカテゴリ別オプション一覧で返却
    
    Returns:
        {
            "Database": ["sqlite", "postgres", "mysql"],
            "VectorStore": ["chroma", "weaviate"], 
            "LLM": ["openai", "anthropic", "ollama"]
        }
    """
```

### 2. has_category()

```python
def has_category(category: str) -> bool:
    """
    指定カテゴリの存在確認
    
    Args:
        category: 確認するカテゴリ名
        
    Returns:
        カテゴリが存在する場合True
    """
```

### 3. get_options()

```python
def get_options(category: str) -> List[str]:
    """
    カテゴリ内の全オプション取得
    
    Args:
        category: 対象カテゴリ名
        
    Returns:
        オプション名のリスト（存在しない場合は空リスト）
    """
```

### 4. generate_template()

```python
def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str:
    """
    選択的テンプレート生成（利用側が直接指定）
    
    Args:
        dest: 出力先ファイルパス
        generation_range: 生成範囲指定
            [
                {"category": "Database", "option": "postgres"},
                {"category": "VectorStore", "option": "chroma"},
                {"category": "LLM"}  # option省略=カテゴリ内全オプション
            ]
        
    Returns:
        生成されたテンプレート内容
    """
```

## 実装例

### 新形式テンプレート関数

```python
# mypackage/templates.py
def database_template():
    return [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLiteデータベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            },
            "description": "軽量なSQLiteデータベース",
            "tags": ["sql", "embedded", "lightweight"]
        },
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
            },
            "description": "強力なPostgreSQLデータベース",
            "tags": ["sql", "relational", "production"]
        }
    ]
```

### 利用側パッケージでの使用例

```python
# 利用側パッケージがRAGアプリケーション用の設定を生成
import oneenv

# 1. 利用可能な構成を把握
structure = oneenv.get_all_template_structure()
print("利用可能な構成:", structure)
# {
#   "Database": ["sqlite", "postgres", "mysql"],
#   "VectorStore": ["chroma", "weaviate"], 
#   "LLM": ["openai", "anthropic", "ollama"]
# }

# 2. 特定の構成確認
if oneenv.has_category("VectorStore"):
    vs_options = oneenv.get_options("VectorStore")
    print("VectorStoreオプション:", vs_options)

# 3. RAGアプリ用の設定生成（利用側が決定）
generation_range = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM"}  # option省略=全LLMオプション
]

# テンプレート生成
template_content = oneenv.generate_template("rag_app.env", generation_range)
```

## バリデーション規則

### EnvOption検証

1. **category/option一意性**: 同一ソース内で同じcategory+optionの組み合わせは禁止
2. **env必須性**: 少なくとも1つの環境変数を定義
3. **依存関係循環チェック**: dependenciesで循環参照を検出
4. **既存EnvVarConfig検証**: envの各値は既存バリデーション規則に従う

### ScaffoldingTemplate検証

1. **options必須性**: 少なくとも1つのEnvOptionを含む
2. **source一意性**: グローバルで同じsourceは禁止
3. **カテゴリ一貫性**: 提供するオプションが適切にカテゴリ分けされている

## メリット・影響

### メリット

1. **インタラクティブ選択**: RAG等の複雑なスタックを段階的に選択可能
2. **構造化設定**: カテゴリ/オプションによる明確な構造
3. **拡張性**: 新しいカテゴリ/オプションを容易に追加
4. **互換性**: 既存システムとの共存可能

### 既存システムへの影響

1. **ゼロ影響**: 既存`@oneenv`デコレータは変更なしで動作継続
2. **段階移行**: 新形式は任意採用、旧形式との混在可能
3. **API拡張**: 新APIは追加のみ、既存API変更なし

## 次ステップ

1. **ユーザー確認**: この設計書の承認
2. **プロトタイプ実装**: 基本的なデータモデル実装
3. **テスト作成**: 新モデルの単体テスト
4. **互換性検証**: 既存システムとの共存テスト