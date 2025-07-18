# OneEnv Scaffolding API リファレンス

## 概要

OneEnv Scaffolding APIは、環境変数テンプレートをカテゴリとオプションで整理する拡張テンプレートシステムへのプログラマティックアクセスを提供します。このAPIにより、開発者はOneEnvのテンプレート発見・生成機能を活用するカスタムツール、スクリプト、アプリケーションを作成できます。

## コア関数

### `oneenv.get_all_template_structure()`

利用可能な全テンプレートの完全な構造をカテゴリとオプションで整理して返します。

**シグネチャ:**
```python
def get_all_template_structure() -> Dict[str, List[str]]
```

**パラメータ:**
- なし

**戻り値:**
- `Dict[str, List[str]]`: カテゴリ名を利用可能なオプションリストにマッピングした辞書

**例:**
```python
import oneenv

structure = oneenv.get_all_template_structure()
print(structure)
# 出力: {
#     'Database': ['postgres', 'sqlite', 'mysql'],
#     'VectorStore': ['chroma', 'pinecone', 'weaviate'],
#     'LLM': ['openai', 'anthropic', 'local'],
#     'Cache': ['redis', 'memcached'],
#     'Monitoring': ['basic', 'advanced']
# }
```

**使用上の注意:**
- この関数はOneEnvテンプレートを持つインストール済みパッケージを全てスキャンします
- パフォーマンスのため結果はキャッシュされます
- Scaffoldingテンプレートが利用できない場合は空の辞書を返します
- カテゴリとオプションはアルファベット順でソートされます

---

### `oneenv.has_category(category)`

指定されたカテゴリが利用可能なテンプレートに存在するかチェックします。

**シグネチャ:**
```python
def has_category(category: str) -> bool
```

**パラメータ:**
- `category` (str): チェックするカテゴリ名

**戻り値:**
- `bool`: カテゴリが存在する場合はTrue、そうでなければFalse

**例:**
```python
import oneenv

if oneenv.has_category("Database"):
    print("Databaseテンプレートが利用可能です")
else:
    print("Databaseテンプレートが見つかりません")

# 複数のカテゴリをチェック
categories_to_check = ["Database", "VectorStore", "NonExistent"]
for cat in categories_to_check:
    status = "✅" if oneenv.has_category(cat) else "❌"
    print(f"{status} {cat}")
```

**使用上の注意:**
- 大文字小文字を区別するカテゴリマッチング
- None や空文字列の入力に対してはFalseを返します
- 他のカテゴリ固有関数を呼び出す前の検証に有用です

---

### `oneenv.get_options(category)`

指定されたカテゴリで利用可能な全オプションを返します。

**シグネチャ:**
```python
def get_options(category: str) -> List[str]
```

**パラメータ:**
- `category` (str): オプションを取得するカテゴリ名

**戻り値:**
- `List[str]`: カテゴリで利用可能なオプションのリスト

**例外:**
- `ValueError`: カテゴリが存在しない場合

**例:**
```python
import oneenv

try:
    options = oneenv.get_options("Database")
    print(f"Databaseオプション: {options}")
    # 出力: ['postgres', 'sqlite', 'mysql']
    
    for option in options:
        print(f"  • {option}")
        
except ValueError as e:
    print(f"エラー: {e}")
```

**使用上の注意:**
- 例外を避けるため、事前に `has_category()` でチェックしてください
- オプションはアルファベット順でソートされます
- カテゴリが存在してもオプションがない場合は空のリストを返します

---

### `oneenv.generate_template(dest, generation_range)`

選択されたカテゴリとオプションに基づいて、カスタマイズされた環境テンプレートファイルを生成します。

**シグネチャ:**
```python
def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str
```

**パラメータ:**
- `dest` (str): 生成されるテンプレートの保存先ファイルパス
- `generation_range` (List[Dict[str, str]]): カテゴリ/オプション選択のリスト

**戻り値:**
- `str`: 生成されたテンプレートの内容

**Generation Range 形式:**
各選択辞書には以下が含まれる必要があります:
- `category` (str): カテゴリ名
- `option` (str): カテゴリ内のオプション名

**例:**
```python
import oneenv

# 選択を定義
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"},
    {"category": "Cache", "option": "redis"}
]

# テンプレート生成
content = oneenv.generate_template(".env.example", selections)
print("生成されたテンプレート内容:")
print(content)
```

**生成される出力形式:**
```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database (postgres) -----
# PostgreSQL connection URL
# Required | Critical
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM (openai) -----
# OpenAI API key for text generation
# Required | Critical
OPENAI_API_KEY=

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Database (postgres) -----
# Connection pool size
# Optional | Important
DATABASE_POOL_SIZE=10

# ----- Cache (redis) -----
# Redis connection URL
# Optional | Important
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Database (postgres) -----
# SSL mode for connections
# Optional | Optional
# Choices: require, prefer, disable
DATABASE_SSL_MODE=prefer
```

**使用上の注意:**
- テンプレート内容は重要度順に整理されます: Critical → Important → Optional
- 各重要度レベル内で、変数はカテゴリ別にグループ化されます
- コメントには説明、必須状態、選択肢（該当する場合）が含まれます
- 指定された保存先パスでファイルが作成/上書きされます

---

## 情報取得関数

### `oneenv.get_structure_info()`

全体のテンプレート構造に関する詳細情報を返します。

**シグネチャ:**
```python
def get_structure_info() -> Dict[str, Any]
```

**パラメータ:**
- なし

**戻り値:**
- `Dict[str, Any]`: 詳細な構造情報

**例:**
```python
import oneenv

info = oneenv.get_structure_info()
print(f"総カテゴリ数: {info['total_categories']}")
print(f"総オプション数: {info['total_options']}")
print(f"総変数数: {info['total_variables']}")

# 出力例:
# {
#     'total_categories': 5,
#     'total_options': 12,
#     'total_variables': 45,
#     'categories': {
#         'Database': {'options': 3, 'variables': 8},
#         'VectorStore': {'options': 3, 'variables': 12},
#         'LLM': {'options': 3, 'variables': 9},
#         'Cache': {'options': 2, 'variables': 6},
#         'Monitoring': {'options': 2, 'variables': 10}
#     }
# }
```

---

### `oneenv.get_category_info(category)`

特定のカテゴリに関する詳細情報を返します。

**シグネチャ:**
```python
def get_category_info(category: str) -> Dict[str, Any]
```

**パラメータ:**
- `category` (str): 情報を取得するカテゴリ名

**戻り値:**
- `Dict[str, Any]`: オプションと変数数を含むカテゴリ情報

**例外:**
- `ValueError`: カテゴリが存在しない場合

**例:**
```python
import oneenv

try:
    info = oneenv.get_category_info("Database")
    print(f"カテゴリ: {info['category']}")
    print(f"オプション: {info['options']}")
    print(f"総変数数: {info['total_variables']}")
    print(f"Critical変数数: {info['critical_variables']}")
    print(f"Important変数数: {info['important_variables']}")
    print(f"Optional変数数: {info['optional_variables']}")
    
    # 出力例:
    # {
    #     'category': 'Database',
    #     'options': ['postgres', 'sqlite', 'mysql'],
    #     'total_variables': 8,
    #     'critical_variables': 3,
    #     'important_variables': 3,
    #     'optional_variables': 2,
    #     'description': 'Database connection and configuration templates'
    # }
    
except ValueError as e:
    print(f"エラー: {e}")
```

---

### `oneenv.get_option_preview(category, option)`

特定のオプションで生成される変数のプレビューを返します。

**シグネチャ:**
```python
def get_option_preview(category: str, option: str) -> Dict[str, Any]
```

**パラメータ:**
- `category` (str): カテゴリ名
- `option` (str): カテゴリ内のオプション名

**戻り値:**
- `Dict[str, Any]`: 変数と設定を含むプレビュー情報

**例外:**
- `ValueError`: カテゴリまたはオプションが存在しない場合

**例:**
```python
import oneenv

try:
    preview = oneenv.get_option_preview("Database", "postgres")
    print(f"プレビュー: {preview['category']} → {preview['option']}")
    print(f"変数数: {len(preview['variables'])}")
    
    for var_name, var_config in preview['variables'].items():
        importance = var_config['importance']
        required = "Required" if var_config['required'] else "Optional"
        print(f"  {var_name}: {required} | {importance.title()}")
        print(f"    {var_config['description']}")
        print(f"    デフォルト: {var_config['default']}")
        if 'choices' in var_config:
            print(f"    選択肢: {var_config['choices']}")
        print()
        
except ValueError as e:
    print(f"エラー: {e}")
```

---

## CLI統合関数

### `oneenv.cli_structure_display()`

CLI表示用にテンプレート構造をフォーマットします。

**シグネチャ:**
```python
def cli_structure_display(json_output: bool = False) -> str
```

**パラメータ:**
- `json_output` (bool): JSON形式で返すかどうか（デフォルト: False）

**戻り値:**
- `str`: フォーマットされた構造表示

**例:**
```python
import oneenv

# テーブル形式
table_output = oneenv.cli_structure_display()
print(table_output)

# JSON形式
json_output = oneenv.cli_structure_display(json_output=True)
print(json_output)
```

---

### `oneenv.cli_category_display(category)`

CLI表示用にカテゴリ情報をフォーマットします。

**シグネチャ:**
```python
def cli_category_display(category: str, json_output: bool = False) -> str
```

**パラメータ:**
- `category` (str): 表示するカテゴリ名
- `json_output` (bool): JSON形式で返すかどうか（デフォルト: False）

**戻り値:**
- `str`: フォーマットされたカテゴリ情報

**例:**
```python
import oneenv

# 人間が読みやすい形式
info = oneenv.cli_category_display("Database")
print(info)

# JSON形式
json_info = oneenv.cli_category_display("Database", json_output=True)
print(json_info)
```

---

### `oneenv.cli_option_preview(category, option)`

CLI表示用にオプションプレビューをフォーマットします。

**シグネチャ:**
```python
def cli_option_preview(category: str, option: str) -> str
```

**パラメータ:**
- `category` (str): カテゴリ名
- `option` (str): オプション名

**戻り値:**
- `str`: フォーマットされたオプションプレビュー

**例:**
```python
import oneenv

preview = oneenv.cli_option_preview("Database", "postgres")
print(preview)
```

---

## エラーハンドリング

### 例外の種類

Scaffolding APIでは以下の例外を使用します:

#### `ValueError`
無効なパラメータが提供された場合に発生:
- カテゴリが存在しない
- オプションがカテゴリに存在しない
- 無効なgeneration_range形式

#### `FileNotFoundError`
テンプレート保存先パスが無効な場合に発生

#### `PermissionError`
テンプレートファイルの書き込み権限が不十分な場合に発生

### エラーハンドリングのベストプラクティス

```python
import oneenv

def safe_template_generation(selections, output_file):
    """適切なエラーハンドリングでテンプレート生成"""
    try:
        # 最初に選択を検証
        for selection in selections:
            if not oneenv.has_category(selection['category']):
                raise ValueError(f"カテゴリ '{selection['category']}' が見つかりません")
            
            options = oneenv.get_options(selection['category'])
            if selection['option'] not in options:
                raise ValueError(f"オプション '{selection['option']}' がカテゴリ '{selection['category']}' に見つかりません")
        
        # テンプレート生成
        content = oneenv.generate_template(output_file, selections)
        return content
        
    except ValueError as e:
        print(f"検証エラー: {e}")
        
        # 有用な提案を提供
        structure = oneenv.get_all_template_structure()
        print(f"利用可能なカテゴリ: {list(structure.keys())}")
        
        return None
        
    except PermissionError as e:
        print(f"権限エラー: {e}")
        print("ファイル権限を確認して再試行してください")
        return None
        
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return None
```

---

## パフォーマンス考慮事項

### キャッシュ機能

APIはパフォーマンスのためにインテリジェントなキャッシュを実装しています:

```python
# 構造は最初の呼び出し後にキャッシュされます
structure = oneenv.get_all_template_structure()  # 遅い - パッケージをスキャン
structure = oneenv.get_all_template_structure()  # 高速 - キャッシュを使用

# パッケージが変更されると、キャッシュは自動的に無効化されます
```

### バッチ処理

複数の操作には、バッチ呼び出しを使用してパフォーマンスを向上させます:

```python
# 効率的なアプローチ
structure = oneenv.get_all_template_structure()
for category in structure.keys():
    options = oneenv.get_options(category)
    # オプションを処理...

# 非効率的なアプローチ
for category in ["Database", "VectorStore", "LLM"]:
    if oneenv.has_category(category):  # 各呼び出しでパッケージをスキャンする可能性
        options = oneenv.get_options(category)
```

---

## 統合例

### カスタムCLIツール

```python
#!/usr/bin/env python3
"""カスタムscaffoldingツール"""

import oneenv
import argparse

def main():
    parser = argparse.ArgumentParser(description="カスタムOneEnv Scaffoldingツール")
    parser.add_argument("--list", action="store_true", help="利用可能なテンプレートをリスト表示")
    parser.add_argument("--info", help="カテゴリ情報を表示")
    parser.add_argument("--preview", nargs=2, metavar=("CATEGORY", "OPTION"), 
                       help="オプションをプレビュー")
    parser.add_argument("--generate", nargs="+", metavar="CATEGORY:OPTION",
                       help="テンプレートを生成")
    
    args = parser.parse_args()
    
    if args.list:
        print(oneenv.cli_structure_display())
    elif args.info:
        print(oneenv.cli_category_display(args.info))
    elif args.preview:
        category, option = args.preview
        print(oneenv.cli_option_preview(category, option))
    elif args.generate:
        selections = []
        for item in args.generate:
            category, option = item.split(":")
            selections.append({"category": category, "option": option})
        
        content = oneenv.generate_template(".env.custom", selections)
        print("✅ カスタムテンプレートの生成に成功しました！")

if __name__ == "__main__":
    main()
```

### インタラクティブセットアップウィザード

```python
#!/usr/bin/env python3
"""インタラクティブセットアップウィザード"""

import oneenv

def interactive_setup():
    """インタラクティブセットアップウィザード"""
    print("🚀 OneEnv インタラクティブセットアップウィザード")
    print("=" * 40)
    
    structure = oneenv.get_all_template_structure()
    selections = []
    
    for category, options in structure.items():
        print(f"\n📁 {category} カテゴリ:")
        
        # カテゴリ情報を表示
        try:
            info = oneenv.get_category_info(category)
            print(f"利用可能なオプション: {', '.join(info['options'])}")
            print(f"総変数数: {info['total_variables']}")
        except ValueError:
            pass
        
        # オプションを表示
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        # ユーザーの選択を取得
        while True:
            choice = input(f"オプションを選択 (1-{len(options)}、またはskip): ")
            if choice.lower() == 'skip':
                break
            
            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    selected_option = options[choice_num - 1]
                    selections.append({
                        "category": category,
                        "option": selected_option
                    })
                    print(f"✅ 選択: {category} → {selected_option}")
                    break
                else:
                    print("無効な選択です。再度お試しください。")
            except ValueError:
                print("有効な数字を入力してください。")
    
    if selections:
        print(f"\n🎯 設定を生成中...")
        content = oneenv.generate_template(".env.wizard", selections)
        print("✅ 設定が生成されました: .env.wizard")
        
        print("\n📋 あなたの選択:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
    else:
        print("選択がありませんでした。")

if __name__ == "__main__":
    interactive_setup()
```

### Web API統合

```python
from flask import Flask, jsonify, request
import oneenv

app = Flask(__name__)

@app.route('/api/structure', methods=['GET'])
def get_structure():
    """テンプレート構造を取得"""
    try:
        structure = oneenv.get_all_template_structure()
        return jsonify(structure)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/category/<category>', methods=['GET'])
def get_category(category):
    """カテゴリ情報を取得"""
    try:
        info = oneenv.get_category_info(category)
        return jsonify(info)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/api/generate', methods=['POST'])
def generate_template():
    """選択からテンプレートを生成"""
    try:
        selections = request.json.get('selections', [])
        content = oneenv.generate_template('.env.generated', selections)
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## バージョン互換性

### サポートされるPythonバージョン
- Python 3.8+
- 依存関係: `pydantic`, `python-dotenv`

### API安定性
- **安定**: コア関数 (`get_all_template_structure`, `has_category`, `get_options`, `generate_template`)
- **安定**: 情報関数 (`get_category_info`, `get_option_preview`)
- **安定**: CLI統合関数

### 下位互換性
- レガシーテンプレート形式は引き続き動作
- 既存のOneEnv APIは変更なし
- 新しいAPI関数は追加のみ

---

## 次のステップ

- **カスタムツールの作成**: これらのAPIを使用してカスタムscaffoldingツールを構築
- **CI/CDとの統合**: デプロイメントパイプラインで環境セットアップを自動化
- **Webインターフェースの構築**: Webベースのテンプレートジェネレーターを作成
- **パッケージ開発**: あなたのエコシステム用の新しいテンプレートパッケージを作成

さらなる例とチュートリアルについては以下を参照してください:
- [Scaffolding使用ガイド](../user-guides/scaffolding-usage_ja.md)
- [ツール作成チュートリアル](../tutorials/10-scaffolding-tool-creation_ja.md)
- [実践例](../tutorials/11-practical-guide_ja.md)