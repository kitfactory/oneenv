# Phase 3: CLI統合・情報提供API詳細仕様書

## 概要

OneEnvのCLI機能を拡張し、パッケージ側が独自のscaffoldingコマンドを作成できるよう、構造化された情報提供に特化したAPIを提供する。

## 設計方針

### 🎯 基本コンセプト
- **情報提供に特化**: OneEnv自体はscaffoldingロジックを持たない
- **パッケージ側の自由度**: 各パッケージが独自の選択UIを実装可能
- **標準化された情報形式**: 構造化されたメタデータの提供

### 📋 想定ユースケース

```python
# パッケージ側でのスクリプト例
import oneenv

# 利用可能な構造を取得
structure = oneenv.get_all_template_structure()
print("Available categories:", list(structure.keys()))

# 特定カテゴリの詳細情報
if oneenv.has_category("Database"):
    options = oneenv.get_options("Database")
    print(f"Database options: {options}")

# ユーザー選択後にテンプレート生成
user_selection = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"}
]
content = oneenv.generate_template("", user_selection)
```

## Phase 3.1: `oneenv template`サブコマンド拡張

### 🎯 新機能

#### 1. `oneenv template --structure`
**利用可能なカテゴリ/オプション構造を表示**

```bash
$ oneenv template --structure
Available Template Structure:
├── Database
│   ├── postgres (3 variables)
│   ├── mysql (2 variables) 
│   └── sqlite (1 variable)
├── VectorStore
│   ├── chroma (4 variables)
│   ├── weaviate (3 variables)
│   └── pinecone (2 variables)
└── Cache
    ├── redis (3 variables)
    └── memcached (2 variables)

Total: 3 categories, 8 options, 20 variables
```

**JSON出力サポート:**
```bash
$ oneenv template --structure --json
{
  "categories": {
    "Database": {
      "options": ["postgres", "mysql", "sqlite"],
      "variable_counts": {"postgres": 3, "mysql": 2, "sqlite": 1}
    },
    "VectorStore": {
      "options": ["chroma", "weaviate", "pinecone"],
      "variable_counts": {"chroma": 4, "weaviate": 3, "pinecone": 2}
    }
  },
  "summary": {
    "total_categories": 3,
    "total_options": 8,
    "total_variables": 20
  }
}
```

#### 2. `oneenv template --info <category>`
**カテゴリ詳細情報の表示**

```bash
$ oneenv template --info Database
Category: Database
Description: Database connection and configuration options

Available Options:
├── postgres
│   ├── DATABASE_URL (required, critical)
│   ├── DATABASE_POOL_SIZE (optional, optional)
│   └── DATABASE_SSL_MODE (optional, important)
├── mysql
│   ├── DATABASE_URL (required, critical)
│   └── DATABASE_CHARSET (optional, optional)
└── sqlite
    └── DATABASE_URL (required, critical)

Variables Summary:
- Critical: 3 variables
- Important: 1 variable  
- Optional: 3 variables
```

#### 3. `oneenv template --preview <category> <option>`
**特定オプションのプレビュー**

```bash
$ oneenv template --preview Database postgres
Preview: Database -> postgres

# ========== CRITICAL: Essential Settings ==========

# ----- Database (postgres) -----

# PostgreSQL connection URL
# Example: postgresql://user:pass@localhost:5432/dbname
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# ========== OPTIONAL: Fine-tuning Settings ==========

# ----- Database (postgres) -----

# Connection pool size for PostgreSQL
DATABASE_POOL_SIZE=10

# SSL mode for PostgreSQL connections
# Choices: require, prefer, disable
DATABASE_SSL_MODE=prefer
```

### 🛠️ 実装詳細

#### CLI引数パーサー拡張

```python
# src/oneenv/cli.py の拡張案
def add_template_subcommands(parser):
    template_parser = parser.add_parser('template', help='Environment template operations')
    template_group = template_parser.add_mutually_exclusive_group()
    
    template_group.add_argument('--structure', action='store_true',
                              help='Show available template structure')
    template_group.add_argument('--info', metavar='CATEGORY',
                              help='Show detailed info for a category')
    template_group.add_argument('--preview', nargs=2, metavar=('CATEGORY', 'OPTION'),
                              help='Preview specific option template')
    
    template_parser.add_argument('--json', action='store_true',
                                help='Output in JSON format')
    template_parser.add_argument('--output', '-o', 
                                help='Output file (default: stdout)')
```

#### ヘルパー関数実装

```python
# src/oneenv/info_api.py (新規ファイル)
def get_structure_info(json_format: bool = False) -> Union[str, Dict]:
    """構造情報を取得"""
    
def get_category_info(category: str, json_format: bool = False) -> Union[str, Dict]:
    """カテゴリ詳細情報を取得"""
    
def get_option_preview(category: str, option: str) -> str:
    """オプションプレビューを取得"""
```

## Phase 3.2: プログラマティックAPI強化

### 🎯 パッケージ開発者向けヘルパー

#### 1. 構造化情報取得API

```python
# 既存APIの拡張
def get_detailed_structure() -> Dict[str, Any]:
    """
    詳細な構造情報を取得
    
    Returns:
        {
            "categories": {
                "Database": {
                    "options": ["postgres", "mysql"],
                    "descriptions": {...},
                    "variable_counts": {...},
                    "importance_distribution": {...}
                }
            },
            "metadata": {
                "total_categories": 3,
                "total_options": 8,
                "total_variables": 20,
                "last_updated": "2024-01-01T00:00:00Z"
            }
        }
    """

def get_option_metadata(category: str, option: str) -> Dict[str, Any]:
    """
    特定オプションの詳細メタデータを取得
    
    Returns:
        {
            "category": "Database",
            "option": "postgres", 
            "variables": {
                "DATABASE_URL": {
                    "description": "...",
                    "required": True,
                    "importance": "critical",
                    "default": "...",
                    "choices": None
                }
            },
            "summary": {
                "total_variables": 3,
                "required_count": 1,
                "importance_counts": {"critical": 1, "important": 0, "optional": 2}
            }
        }
    """
```

#### 2. バリデーション支援API

```python
def validate_selection(selection: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    選択の妥当性を検証
    
    Returns:
        {
            "valid": True,
            "warnings": ["Option 'mysql' in category 'Database' has been deprecated"],
            "errors": [],
            "suggestions": ["Consider using 'postgres' instead of 'mysql'"],
            "conflicts": []
        }
    """

def suggest_completion(partial_selection: List[Dict[str, str]]) -> List[str]:
    """
    不完全な選択に対する補完候補を提案
    
    Returns:
        ["Consider adding VectorStore option for complete RAG setup",
         "Cache option recommended for better performance"]
    """
```

#### 3. スクリプト作成支援

```python
def generate_script_template(
    categories: List[str],
    script_type: str = "interactive"
) -> str:
    """
    パッケージ側スクリプトのテンプレート生成
    
    Args:
        categories: 対象カテゴリリスト
        script_type: "interactive" | "cli" | "config_file"
    
    Returns:
        生成されたPythonスクリプトのテンプレート
    """
```

### 📝 生成されるスクリプト例

```python
# 生成されるinteractiveスクリプトの例
import oneenv

def interactive_scaffold():
    """Interactive scaffolding for MyRAGProject"""
    
    print("🚀 MyRAGProject Environment Setup")
    print("=" * 40)
    
    # Get available structure
    structure = oneenv.get_all_template_structure()
    
    selections = []
    
    # Database selection
    if "Database" in structure:
        print("\n📊 Database Configuration:")
        db_options = oneenv.get_options("Database")
        for i, option in enumerate(db_options, 1):
            print(f"  {i}. {option}")
        
        choice = input("Select database (1-{}): ".format(len(db_options)))
        selections.append({
            "category": "Database",
            "option": db_options[int(choice) - 1]
        })
    
    # Generate template
    if selections:
        content = oneenv.generate_template(".env.example", selections)
        print(f"\n✅ Generated .env.example with {len(selections)} selections")
    
if __name__ == "__main__":
    interactive_scaffold()
```

## CLI使用例

### 🎯 パッケージ開発者の使用フロー

```bash
# 1. 利用可能な構造を確認
$ oneenv template --structure
Available Template Structure:
├── Database (3 options)
├── VectorStore (3 options)
└── Cache (2 options)

# 2. 特定カテゴリの詳細を確認
$ oneenv template --info Database
Category: Database
Available Options: postgres, mysql, sqlite
Variables: 6 total (3 critical, 1 important, 2 optional)

# 3. 特定オプションをプレビュー
$ oneenv template --preview Database postgres
# [プレビュー出力]

# 4. JSON形式で構造を取得（スクリプト作成用）
$ oneenv template --structure --json > structure.json

# 5. パッケージ独自スクリプトの作成・実行
$ python my_scaffold.py  # パッケージが提供
```

## README更新内容

### 新セクション追加案

```markdown
## Advanced Usage: Package-specific Scaffolding 🛠️

OneEnv provides structured information for packages to create custom scaffolding tools:

### Get Available Structure
```bash
# View all available categories and options
oneenv template --structure

# Get specific category details  
oneenv template --info Database

# Preview specific option
oneenv template --preview Database postgres
```

### For Package Developers
Create custom scaffolding scripts using OneEnv's information APIs:

```python
import oneenv

# Get structured information
structure = oneenv.get_all_template_structure()
metadata = oneenv.get_detailed_structure()

# Build your custom selection UI
user_selection = custom_selection_ui(structure)

# Generate template
oneenv.generate_template(".env.example", user_selection)
```
```

## 成功基準

### 機能面
- ✅ `--structure`, `--info`, `--preview`オプションの正常動作
- ✅ JSON出力形式の正確性
- ✅ プログラマティックAPIの一貫性

### ユーザビリティ面
- ✅ 分かりやすい構造表示
- ✅ パッケージ開発者が簡単にスクリプト作成可能
- ✅ 明確なドキュメントと例

### エコシステム面
- ✅ パッケージ間での一貫した情報形式
- ✅ 既存機能との後方互換性
- ✅ 拡張性のあるAPI設計

## 次のステップ

1. **ユーザー確認**: この仕様に対するフィードバック取得
2. **実装計画**: 段階的な機能実装
3. **README更新**: 新機能の説明追加
4. **サンプル作成**: パッケージ開発者向けの例

---

**注意**: この設計は情報提供に特化し、パッケージ側の自由度を最大化することを重視しています。