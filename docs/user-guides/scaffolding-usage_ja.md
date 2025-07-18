# OneEnv Scaffolding System ユーザーガイド

## 概要

OneEnv Scaffolding Systemは、インストールされたパッケージから環境設定ファイルを自動的に発見、整理、生成するための強力な機能です。手動で`.env`ファイルを作成する代わりに、システムがカテゴリやオプションによってテンプレートを知的に構造化し、環境管理をより直感的で拡張可能にします。

### Scaffoldingとは？

OneEnvにおける**Scaffolding**とは、以下の自動化されたプロセスを指します：
- **発見**: インストールされたパッケージから環境変数テンプレートを発見
- **整理**: カテゴリ別（Database、VectorStore、LLMなど）に整理
- **提供**: カスタムツール作成のための構造化情報を提供
- **生成**: ユーザーの選択に基づいてカスタマイズされた`.env`ファイルを生成

### 主な利点

✅ **知的な整理**: テンプレートが技術カテゴリごとにグループ化  
✅ **選択的生成**: 必要な設定のみを生成  
✅ **重要度階層**: 変数がCritical/Important/Optionalで分類  
✅ **ツールフレンドリー**: カスタムscaffoldingツール作成用のAPI設計  
✅ **拡張可能**: 新しいテンプレートとカテゴリを簡単に追加  

### Scaffoldingを使用する場面

- **新規プロジェクト立ち上げ**: 新しいプロジェクトの環境変数を素早く設定
- **マルチサービスアプリケーション**: 複雑なシステム（RAG、マイクロサービス）の設定管理
- **ツール開発**: パッケージ用のカスタムセットアップウィザードを作成
- **チーム標準化**: チーム間での一貫した環境設定を保証

## 基本的な使用方法

### 1. 利用可能なテンプレートの探索

#### 全カテゴリとオプションの表示
```bash
oneenv template --structure
```

**出力：**
```
Available template structure:
┌─────────────────┬─────────────────────────────────────┐
│ Category        │ Options                             │
├─────────────────┼─────────────────────────────────────┤
│ Database        │ postgres, sqlite, mysql             │
│ VectorStore     │ chroma, pinecone, weaviate          │
│ LLM             │ openai, anthropic, local            │
│ Cache           │ redis, memcached                    │
│ Monitoring      │ basic, advanced                     │
└─────────────────┴─────────────────────────────────────┘
```

#### カテゴリの詳細情報取得
```bash
oneenv template --info Database
```

**出力：**
```
Database Category Information:
- Available options: postgres, sqlite, mysql
- Total variables: 8
- Critical variables: 3
- Important variables: 3
- Optional variables: 2

Description: Database connection and configuration templates
Common use cases: Web applications, data processing, analytics
```

#### 特定オプションのプレビュー
```bash
oneenv template --preview Database postgres
```

**出力：**
```
Preview: Database → postgres
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PostgreSQL connection URL
# Required | Critical
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# Connection pool size
# Optional | Important
DATABASE_POOL_SIZE=10

# SSL mode for connections
# Optional | Optional
# Choices: require, prefer, disable
DATABASE_SSL_MODE=prefer
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 2. テンプレート構造の理解

テンプレートは階層構造で整理されています：

```
カテゴリ（例：「Database」）
├── オプション（例：「postgres」）
│   ├── 変数1（例：「DATABASE_URL」）
│   ├── 変数2（例：「DATABASE_POOL_SIZE」）
│   └── 変数3（例：「DATABASE_SSL_MODE」）
├── オプション（例：「sqlite」）
│   ├── 変数1（例：「DATABASE_URL」）
│   └── 変数2（例：「DATABASE_TIMEOUT」）
└── オプション（例：「mysql」）
    ├── 変数1（例：「DATABASE_URL」）
    └── 変数2（例：「DATABASE_CHARSET」）
```

### 3. 基本的なテンプレート生成

#### 標準のテンプレートコマンド使用
```bash
oneenv template
```

これにより、重要度別に整理された利用可能な全テンプレートを含む`.env.example`ファイルが生成されます：

```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database -----
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM -----
OPENAI_API_KEY=

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Cache -----
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Monitoring -----
LOG_LEVEL=INFO
```

## 高度な使用方法

### 1. プログラマティックAPI使用

#### 基本的な情報取得
```python
import oneenv

# 利用可能な全構造を取得
structure = oneenv.get_all_template_structure()
print(structure)
# 出力: {'Database': ['postgres', 'sqlite'], 'VectorStore': ['chroma', 'pinecone']}

# カテゴリが存在するかチェック
if oneenv.has_category("Database"):
    print("Databaseテンプレートが利用可能です")

# 特定カテゴリのオプションを取得
options = oneenv.get_options("Database")
print(f"Databaseオプション: {options}")
# 出力: ['postgres', 'sqlite', 'mysql']
```

#### 選択的テンプレート生成
```python
# 選択を定義
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

# 選択されたオプションのみでテンプレート生成
content = oneenv.generate_template(".env.example", selections)
print("選択されたオプション用のテンプレートを生成しました")
```

### 2. カスタムScaffoldingツールの作成

#### シンプルなCLIツール
```python
#!/usr/bin/env python3
"""カスタムscaffoldingツール例"""

import oneenv
import argparse

def list_available():
    """利用可能な全テンプレートをリスト表示"""
    structure = oneenv.get_all_template_structure()
    
    print("🔍 利用可能なテンプレート:")
    for category, options in structure.items():
        print(f"\n📁 {category}:")
        for option in options:
            print(f"   • {option}")

def generate_custom(selections):
    """カスタムテンプレートを生成"""
    try:
        content = oneenv.generate_template(".env.custom", selections)
        print("✅ カスタムテンプレートの生成に成功しました！")
        print(f"📁 ファイル: .env.custom")
        
        print("\n📋 選択された設定:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
    except Exception as e:
        print(f"❌ エラー: {e}")

def main():
    parser = argparse.ArgumentParser(description="カスタムOneEnv Scaffoldingツール")
    parser.add_argument("--list", action="store_true", help="利用可能なテンプレートをリスト表示")
    parser.add_argument("--generate", nargs="+", help="テンプレートを生成 (形式: Category:Option)")
    
    args = parser.parse_args()
    
    if args.list:
        list_available()
    elif args.generate:
        selections = []
        for item in args.generate:
            category, option = item.split(":")
            selections.append({"category": category, "option": option})
        generate_custom(selections)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

**使用方法：**
```bash
python custom_scaffold.py --list
python custom_scaffold.py --generate Database:postgres VectorStore:chroma
```

#### インタラクティブウィザード
```python
#!/usr/bin/env python3
"""インタラクティブscaffoldingウィザード"""

import oneenv

def interactive_setup():
    """インタラクティブセットアップウィザード"""
    print("🚀 OneEnv インタラクティブセットアップウィザード")
    print("=" * 40)
    
    structure = oneenv.get_all_template_structure()
    selections = []
    
    for category, options in structure.items():
        print(f"\n📁 {category} カテゴリ:")
        print("利用可能なオプション:")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = input(f"オプションを選択 (1-{len(options)}、またはskip): ")
                if choice.lower() == 'skip':
                    break
                
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

### 3. スクリプト用JSON出力

#### JSON形式での構造取得
```bash
oneenv template --structure --json
```

**出力：**
```json
{
  "Database": ["postgres", "sqlite", "mysql"],
  "VectorStore": ["chroma", "pinecone", "weaviate"],
  "LLM": ["openai", "anthropic", "local"],
  "Cache": ["redis", "memcached"],
  "Monitoring": ["basic", "advanced"]
}
```

#### JSON形式でのカテゴリ情報
```bash
oneenv template --info Database --json
```

**出力：**
```json
{
  "category": "Database",
  "options": ["postgres", "sqlite", "mysql"],
  "total_variables": 8,
  "critical_variables": 3,
  "important_variables": 3,
  "optional_variables": 2,
  "description": "Database connection and configuration templates"
}
```

## 実践的な例

### 1. RAGシステム設定

```python
# Retrieval-Augmented Generation システム用のセットアップ
import oneenv

# RAGコンポーネントを定義
rag_selections = [
    {"category": "Database", "option": "postgres"},      # ドキュメントメタデータ
    {"category": "VectorStore", "option": "chroma"},     # エンベディング
    {"category": "LLM", "option": "openai"},            # テキスト生成
    {"category": "Cache", "option": "redis"},           # レスポンスキャッシュ
    {"category": "Monitoring", "option": "basic"}       # システムモニタリング
]

# RAG固有の設定を生成
content = oneenv.generate_template(".env.rag", rag_selections)
print("RAGシステム設定が生成されました！")
```

### 2. Webアプリケーションセットアップ

```python
# Webアプリケーション用のセットアップ
web_selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "advanced"}
]

content = oneenv.generate_template(".env.web", web_selections)
```

### 3. 開発環境 vs 本番環境

```python
# 開発環境
dev_selections = [
    {"category": "Database", "option": "sqlite"},       # 開発用軽量
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "basic"}
]

# 本番環境
prod_selections = [
    {"category": "Database", "option": "postgres"},     # 本番用堅牢
    {"category": "Cache", "option": "redis"},
    {"category": "Monitoring", "option": "advanced"}   # 包括的モニタリング
]

oneenv.generate_template(".env.development", dev_selections)
oneenv.generate_template(".env.production", prod_selections)
```

## 出力形式の理解

### 重要度ベースの整理

生成されたテンプレートは重要度レベルで整理されます：

#### 1. **CRITICAL** 🚨
アプリケーション動作に不可欠な設定：
- データベース接続URL
- 外部サービスのAPIキー
- 認証シークレット

#### 2. **IMPORTANT** ⚠️
本番環境で設定すべき設定：
- コネクションプールサイズ
- キャッシュ設定
- APIエンドポイント

#### 3. **OPTIONAL** ℹ️
細かい調整設定（デフォルトで十分）：
- タイムアウト値
- デバッグフラグ
- パフォーマンス最適化

### カテゴリベースのグループ化

各重要度レベル内で、変数はカテゴリごとにグループ化されます：

```env
# ========== CRITICAL: Essential Settings for Application Operation ==========

# ----- Database (postgres) -----
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb

# ----- LLM (openai) -----
OPENAI_API_KEY=

# ----- VectorStore (chroma) -----
CHROMA_HOST=localhost

# ========== IMPORTANT: Settings to Configure for Production Use ==========

# ----- Database (postgres) -----
DATABASE_POOL_SIZE=10

# ----- Cache (redis) -----
REDIS_URL=redis://localhost:6379/0

# ========== OPTIONAL: Fine-tuning Settings (Defaults are Sufficient) ==========

# ----- Database (postgres) -----
DATABASE_SSL_MODE=prefer

# ----- LLM (openai) -----
OPENAI_TEMPERATURE=0.7
```

## トラブルシューティング

### よくある問題

#### 1. "No scaffolding templates are currently available"
**原因**: OneEnvテンプレートを持つパッケージがインストールされていない。

**解決方法**:
```bash
# テンプレートを提供するパッケージをインストール
pip install your-package-with-templates

# または独自のテンプレートを作成（チュートリアル9参照）
```

#### 2. "Category 'X' not found"
**原因**: 指定されたカテゴリが利用可能なテンプレートに存在しない。

**解決方法**:
```bash
# 利用可能なカテゴリを確認
oneenv template --structure

# 正しいカテゴリ名を使用
oneenv template --info Database  # "database"ではなく
```

#### 3. "Option 'X' not found in category 'Y'"
**原因**: 指定されたカテゴリにそのオプションが存在しない。

**解決方法**:
```bash
# 利用可能なオプションを確認
oneenv template --info Database

# 正しいオプション名を使用
oneenv template --preview Database postgres  # "postgresql"ではなく
```

#### 4. 空または最小限のテンプレートが生成される
**原因**: 選択に一致するテンプレートがない、またはテンプレートが正しくインストールされていない。

**解決方法**:
```python
# 実際に利用可能なものを確認
import oneenv
structure = oneenv.get_all_template_structure()
print(f"利用可能なテンプレート: {structure}")

# 選択が存在することを確認
for selection in your_selections:
    if not oneenv.has_category(selection['category']):
        print(f"不足しているカテゴリ: {selection['category']}")
```

### パフォーマンスの最適化

#### 1. テンプレート発見のキャッシュ
```python
# 繰り返し使用のため構造をキャッシュ
structure = oneenv.get_all_template_structure()

# 繰り返し呼び出しの代わりにキャッシュされた構造を再利用
for category in structure.keys():
    options = oneenv.get_options(category)
    # オプションを処理...
```

#### 2. バッチ処理
```python
# 複数の選択を一度に処理
all_selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "VectorStore", "option": "chroma"},
    {"category": "LLM", "option": "openai"}
]

# 単一の生成呼び出し
content = oneenv.generate_template(".env.example", all_selections)
```

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
        
    except Exception as e:
        print(f"テンプレート生成エラー: {e}")
        
        # 有用な提案を提供
        structure = oneenv.get_all_template_structure()
        print(f"利用可能なカテゴリ: {list(structure.keys())}")
        
        return None
```

## ベストプラクティス

### 1. テンプレートの整理
- **Criticalから開始**: 常に重要な設定を最初に設定
- **環境固有**: 開発/ステージング/本番で異なるテンプレートを使用
- **モジュラーアプローチ**: 特定のコンポーネント用のテンプレートを別々に生成

### 2. ツール開発
- **ユーザーフレンドリー**: 明確なオプションとフィードバックを提供
- **エラーハンドリング**: 提案付きの有用なエラーメッセージを提供
- **ドキュメント**: 使用例とトラブルシューティングを含める

### 3. チーム連携
- **標準化**: 一貫したカテゴリとオプション名を使用
- **バージョン管理**: テンプレートの変更とバージョンを追跡
- **ドキュメント**: カスタムテンプレートとその目的を文書化

## 次のステップ

- **独自のテンプレート作成**: [チュートリアル9: 新しいテンプレート作成](../tutorials/09-new-template-creation_ja.md)
- **カスタムツールの構築**: [チュートリアル10: Scaffoldingツール作成](../tutorials/10-scaffolding-tool-creation_ja.md)
- **実践例**: [チュートリアル11: 実践ガイド](../tutorials/11-practical-guide_ja.md)
- **APIリファレンス**: [Scaffolding APIリファレンス](../api-reference/scaffolding-api_ja.md)
- **移行ガイド**: [移行ガイド](../migration-guides/scaffolding-format-migration_ja.md)

---

**🎉 おめでとうございます！** OneEnvのScaffolding Systemを効果的に使用して環境設定を管理する方法を理解しました。このシステムは、個人の開発者にもチームにも、開発ワークフローを効率化するための強力なツールを提供します。