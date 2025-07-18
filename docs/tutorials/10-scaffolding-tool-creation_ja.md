# チュートリアル 10: 情報提供APIを使ったScaffoldingツール作成

**所要時間:** 20-25分  
**対象:** ツール作成者、パッケージ開発者  
**前提条件:** Python基礎、CLI開発の知識

## 概要

OneEnvの情報提供APIを使用してカスタムscaffoldingツールを作成する方法を学習します。これらのツールは、特定の用途に合わせたインタラクティブなセットアップ体験を提供できます。

## 学習内容

- OneEnvの情報APIを理解
- シンプルなCLI scaffoldingツールの作成
- インタラクティブな選択ウィザードの構築
- エラーとエッジケースの適切な処理
- 既存ワークフローとの統合

## 1. 情報APIの理解 (5分)

### コアAPI関数

OneEnvはテンプレート情報を取得するための4つの主要関数を提供します：

```python
import oneenv

# 利用可能な全カテゴリとそのオプションを取得
structure = oneenv.get_all_template_structure()
# 戻り値: {"Database": ["postgres", "sqlite"], "Cache": ["redis"]}

# カテゴリの存在確認
has_db = oneenv.has_category("Database")
# 戻り値: True または False

# 特定カテゴリのオプション取得
db_options = oneenv.get_options("Database")
# 戻り値: ["postgres", "sqlite", "mysql"]

# 選択に基づいてテンプレート生成
selections = [
    {"category": "Database", "option": "postgres"},
    {"category": "Cache", "option": "redis"}
]
content = oneenv.generate_template(".env.example", selections)
# 戻り値: 生成されたテンプレート内容
```

### CLI情報コマンド

ツールを構築する前に、利用可能なものを探索しましょう：

```bash
# 利用可能な全構造を表示
oneenv template --structure

# カテゴリ詳細を取得
oneenv template --info Database

# 特定オプションをプレビュー
oneenv template --preview Database postgres

# スクリプト用JSON出力を取得
oneenv template --structure --json
```

## 2. シンプルなCLIツール (8分)

基本的なコマンドラインscaffoldingツールを作成しましょう。

### ステップ1: 基本構造の作成

`simple_scaffold.py`を作成：

```python
#!/usr/bin/env python3
"""シンプルなOneEnv Scaffoldingツール"""

import oneenv
import argparse
import sys
from typing import List, Dict

def list_available_options():
    """利用可能な全カテゴリとオプションを表示"""
    print("🔍 利用可能なテンプレート:")
    print("=" * 30)
    
    try:
        structure = oneenv.get_all_template_structure()
        
        if not structure:
            print("❌ テンプレートが見つかりません。OneEnvテンプレートを持つパッケージを先にインストールしてください。")
            return
        
        for category, options in structure.items():
            print(f"\n📁 {category}:")
            for option in options:
                print(f"   • {option}")
                
    except Exception as e:
        print(f"❌ テンプレート取得エラー: {e}")
        sys.exit(1)

def validate_selection(category: str, option: str) -> bool:
    """カテゴリ/オプションの組み合わせが存在することを検証"""
    if not oneenv.has_category(category):
        print(f"❌ カテゴリ '{category}' が見つかりません。")
        
        # 類似カテゴリを提案
        structure = oneenv.get_all_template_structure()
        available = list(structure.keys())
        print(f"📋 利用可能なカテゴリ: {', '.join(available)}")
        return False
    
    available_options = oneenv.get_options(category)
    if option not in available_options:
        print(f"❌ オプション '{option}' がカテゴリ '{category}' に見つかりません。")
        print(f"📋 利用可能なオプション: {', '.join(available_options)}")
        return False
    
    return True

def generate_template_file(selections: List[Dict[str, str]], output_file: str):
    """選択からテンプレートファイルを生成"""
    print(f"🔨 テンプレート生成中: {output_file}")
    
    try:
        content = oneenv.generate_template(output_file, selections)
        
        print("✅ テンプレートの生成に成功しました！")
        print(f"📁 ファイル: {output_file}")
        print("\n📋 選択された設定:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
        print(f"\n💡 次のステップ:")
        print(f"   1. {output_file}を確認")
        print(f"   2. .envにコピーして値を設定")
        
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="シンプルなOneEnv Scaffoldingツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
例:
  %(prog)s --list
  %(prog)s --generate Database:postgres Cache:redis
  %(prog)s --generate Database:sqlite --output .env.dev
        """
    )
    
    parser.add_argument(
        "--list", 
        action="store_true",
        help="利用可能な全カテゴリとオプションをリスト表示"
    )
    
    parser.add_argument(
        "--generate", 
        nargs="+",
        metavar="CATEGORY:OPTION",
        help="指定されたcategory:optionペアでテンプレートを生成"
    )
    
    parser.add_argument(
        "--output", 
        default=".env.example",
        help="出力ファイル名 (デフォルト: .env.example)"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_available_options()
        return
    
    if args.generate:
        # category:optionペアを解析
        selections = []
        
        for item in args.generate:
            if ":" not in item:
                print(f"❌ 無効な形式: '{item}'。CATEGORY:OPTION形式を使用してください。")
                sys.exit(1)
            
            category, option = item.split(":", 1)
            
            if not validate_selection(category, option):
                sys.exit(1)
            
            selections.append({"category": category, "option": option})
        
        generate_template_file(selections, args.output)
        return
    
    # 引数がない場合はヘルプを表示
    parser.print_help()

if __name__ == "__main__":
    main()
```

### ステップ2: ツールのテスト

```bash
# 実行可能にする
chmod +x simple_scaffold.py

# 利用可能なオプションをリスト表示
./simple_scaffold.py --list

# テンプレートを生成
./simple_scaffold.py --generate Database:postgres Cache:redis

# カスタム出力ファイル
./simple_scaffold.py --generate Database:sqlite --output .env.dev
```

## 3. インタラクティブウィザード (7分)

より良いユーザーエクスペリエンスのため、インタラクティブウィザードを作成しましょう。

### ステップ1: インタラクティブウィザードの作成

`interactive_scaffold.py`を作成：

```python
#!/usr/bin/env python3
"""インタラクティブOneEnv Scaffoldingウィザード"""

import oneenv
import sys
from typing import List, Dict, Optional

class ScaffoldingWizard:
    def __init__(self):
        self.selections: List[Dict[str, str]] = []
        self.structure = {}
        
    def load_templates(self):
        """利用可能なテンプレートを読み込み"""
        try:
            self.structure = oneenv.get_all_template_structure()
            if not self.structure:
                print("❌ テンプレートが見つかりません。OneEnvテンプレートを持つパッケージを先にインストールしてください。")
                sys.exit(1)
        except Exception as e:
            print(f"❌ テンプレート読み込みエラー: {e}")
            sys.exit(1)
    
    def show_welcome(self):
        """ウェルカムメッセージを表示"""
        print("🚀 OneEnv インタラクティブScaffoldingウィザード")
        print("=" * 45)
        print("このウィザードは環境設定の構成をサポートします。")
        print("複数のカテゴリとオプションから選択できます。\n")
    
    def display_categories(self) -> List[str]:
        """利用可能なカテゴリを表示してリストを返す"""
        categories = list(self.structure.keys())
        
        print("📁 利用可能なカテゴリ:")
        for i, category in enumerate(categories, 1):
            options_count = len(self.structure[category])
            print(f"   {i}. {category} ({options_count}個のオプション)")
        
        return categories
    
    def select_category(self) -> Optional[str]:
        """ユーザーにカテゴリを選択させる"""
        categories = self.display_categories()
        
        while True:
            try:
                print(f"\n❓ カテゴリを選択してください (1-{len(categories)}、または0で終了):")
                choice = input("👉 ").strip()
                
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(categories):
                    return categories[choice_num - 1]
                else:
                    print(f"❌ 1から{len(categories)}の間の数字を入力してください")
                    
            except ValueError:
                print("❌ 有効な数字を入力してください")
            except KeyboardInterrupt:
                print("\n👋 さようなら！")
                sys.exit(0)
    
    def display_options(self, category: str) -> List[str]:
        """カテゴリのオプションを表示"""
        options = oneenv.get_options(category)
        
        print(f"\n🔧 {category}の利用可能なオプション:")
        for i, option in enumerate(options, 1):
            # 変数数を表示するためにプレビューを取得
            try:
                preview = oneenv.get_option_preview(category, option)
                var_lines = [line for line in preview.split('\n') 
                           if '=' in line and not line.startswith('#')]
                var_count = len(var_lines)
                print(f"   {i}. {option} ({var_count}個の変数)")
            except:
                print(f"   {i}. {option}")
        
        return options
    
    def select_option(self, category: str) -> Optional[str]:
        """ユーザーにカテゴリからオプションを選択させる"""
        options = self.display_options(category)
        
        while True:
            try:
                print(f"\n❓ オプションを選択してください (1-{len(options)}、または0でスキップ):")
                choice = input("👉 ").strip()
                
                if choice == "0":
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                else:
                    print(f"❌ 1から{len(options)}の間の数字を入力してください")
                    
            except ValueError:
                print("❌ 有効な数字を入力してください")
            except KeyboardInterrupt:
                print("\n👋 さようなら！")
                sys.exit(0)
    
    def show_preview(self, category: str, option: str):
        """選択されたオプションのプレビューを表示"""
        try:
            preview = oneenv.get_option_preview(category, option)
            print(f"\n📋 {category}:{option}のプレビュー:")
            print("-" * 30)
            # 最初の数行のみ表示
            lines = preview.split('\n')[:10]
            for line in lines:
                print(line)
            if len(preview.split('\n')) > 10:
                print("...")
            print("-" * 30)
        except Exception as e:
            print(f"⚠️  プレビューを読み込めませんでした: {e}")
    
    def confirm_selection(self, category: str, option: str) -> bool:
        """ユーザーに選択の確認を求める"""
        self.show_preview(category, option)
        
        while True:
            confirm = input(f"\n✅ {category}:{option}を設定に追加しますか？ (y/n): ").strip().lower()
            if confirm in ['y', 'yes']:
                return True
            elif confirm in ['n', 'no']:
                return False
            else:
                print("❌ 'y'または'n'を入力してください")
    
    def show_current_selections(self):
        """現在の選択を表示"""
        if not self.selections:
            print("\n📝 まだ選択がありません。")
            return
        
        print("\n📝 現在の選択:")
        for i, selection in enumerate(self.selections, 1):
            print(f"   {i}. {selection['category']}: {selection['option']}")
    
    def generate_final_template(self) -> str:
        """最終テンプレートを生成"""
        if not self.selections:
            print("❌ 選択がありません。テンプレートを生成できません。")
            return ""
        
        output_file = input("\n📁 出力ファイル名 (デフォルト: .env.example): ").strip()
        if not output_file:
            output_file = ".env.example"
        
        try:
            content = oneenv.generate_template(output_file, self.selections)
            return output_file
        except Exception as e:
            print(f"❌ テンプレート生成エラー: {e}")
            return ""
    
    def run(self):
        """インタラクティブウィザードを実行"""
        self.load_templates()
        self.show_welcome()
        
        while True:
            self.show_current_selections()
            
            category = self.select_category()
            if category is None:
                break
            
            option = self.select_option(category)
            if option is None:
                continue
            
            if self.confirm_selection(category, option):
                self.selections.append({"category": category, "option": option})
                print(f"✅ {category}:{option}を追加しました")
        
        if self.selections:
            print("\n🎯 設定を確定中...")
            output_file = self.generate_final_template()
            
            if output_file:
                print(f"\n🎉 成功！ {output_file}を生成しました")
                print("\n💡 次のステップ:")
                print(f"   1. {output_file}を確認")
                print("   2. .envにコピーして実際の値を設定")
                print("   3. .envを.gitignoreファイルに追加")
        else:
            print("\n👋 選択がありませんでした。さようなら！")

def main():
    wizard = ScaffoldingWizard()
    wizard.run()

if __name__ == "__main__":
    main()
```

### ステップ2: インタラクティブウィザードのテスト

```bash
# 実行可能にする
chmod +x interactive_scaffold.py

# ウィザードを実行
./interactive_scaffold.py
```

## 4. 高度な機能 (5分)

### 設定ファイルサポート

YAML ベースの設定用に`config_scaffold.py`を作成：

```python
#!/usr/bin/env python3
"""設定ベースのOneEnv Scaffoldingツール"""

import oneenv
import yaml
import argparse
import sys
from typing import Dict, List

def load_config(config_file: str) -> Dict:
    """YAMLファイルから設定を読み込み"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ 設定ファイルが見つかりません: {config_file}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ {config_file}の無効なYAML: {e}")
        sys.exit(1)

def validate_config(config: Dict) -> List[Dict[str, str]]:
    """設定を検証して選択を返す"""
    selections = []
    
    if 'selections' not in config:
        print("❌ 設定には'selections'キーが必要です")
        sys.exit(1)
    
    for item in config['selections']:
        if 'category' not in item or 'option' not in item:
            print(f"❌ 各選択には'category'と'option'が必要です: {item}")
            sys.exit(1)
        
        category = item['category']
        option = item['option']
        
        # OneEnvで検証
        if not oneenv.has_category(category):
            print(f"❌ カテゴリ '{category}' が見つかりません")
            sys.exit(1)
        
        available_options = oneenv.get_options(category)
        if option not in available_options:
            print(f"❌ オプション '{option}' がカテゴリ '{category}' に見つかりません")
            print(f"📋 利用可能: {', '.join(available_options)}")
            sys.exit(1)
        
        selections.append({"category": category, "option": option})
    
    return selections

def create_sample_config():
    """サンプル設定ファイルを作成"""
    sample = {
        'output': '.env.example',
        'selections': [
            {'category': 'Database', 'option': 'postgres'},
            {'category': 'Cache', 'option': 'redis'}
        ]
    }
    
    with open('scaffold.yaml', 'w') as f:
        yaml.dump(sample, f, default_flow_style=False)
    
    print("📝 サンプル設定を作成しました: scaffold.yaml")
    print("💡 このファイルを編集して実行: python config_scaffold.py scaffold.yaml")

def main():
    parser = argparse.ArgumentParser(description="設定ベースのOneEnv Scaffolding")
    parser.add_argument('config', nargs='?', help="YAML設定ファイル")
    parser.add_argument('--sample', action='store_true', help="サンプル設定を作成")
    
    args = parser.parse_args()
    
    if args.sample:
        create_sample_config()
        return
    
    if not args.config:
        parser.print_help()
        return
    
    # 設定を読み込み検証
    config = load_config(args.config)
    selections = validate_config(config)
    
    # テンプレート生成
    output_file = config.get('output', '.env.example')
    
    try:
        oneenv.generate_template(output_file, selections)
        print(f"✅ {args.config}から{output_file}を生成しました")
        
        print("\n📋 適用された設定:")
        for selection in selections:
            print(f"   • {selection['category']}: {selection['option']}")
            
    except Exception as e:
        print(f"❌ テンプレート生成エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### サンプルYAML設定

```yaml
# scaffold.yaml
output: .env.example
selections:
  - category: Database
    option: postgres
  - category: Cache
    option: redis
  - category: VectorStore
    option: chroma
```

## 5. ビルドツールとの統合

### package.jsonスクリプトへの追加

```json
{
  "scripts": {
    "env:setup": "python scripts/scaffold.py",
    "env:interactive": "python scripts/interactive_scaffold.py"
  }
}
```

### Makefileへの追加

```makefile
.PHONY: env-setup
env-setup:
	python scripts/scaffold.py --generate Database:postgres Cache:redis

.PHONY: env-interactive
env-interactive:
	python scripts/interactive_scaffold.py
```

## ベストプラクティス

### 🛡️ エラーハンドリング
- 常にカテゴリ/オプションの組み合わせを検証
- 提案を含む有用なエラーメッセージを提供
- ネットワーク/ファイルシステムエラーを適切に処理

### 🎨 ユーザーエクスペリエンス
- 明確な視覚的インジケータを使用（絵文字、サポートされている場合は色）
- 最終選択前にプレビューを提供
- 進捗と次のステップを表示

### 📦 配布
- shebangラインでツールを実行可能にする
- requirements.txtまたはpyproject.tomlの依存関係を含める
- ヘルプテキストと例を追加

### 🔧 拡張性
- 繰り返し可能なセットアップのため設定ファイルをサポート
- カスタム出力形式を許可
- 既存ワークフローとの統合を有効にする

## 次のステップ

- **例を試す**: プロジェクトで3つのツール全てをテスト
- **チュートリアル11**: 実際のプロジェクトでの現実的な応用を確認
- **カスタマイズ**: 特定のニーズに合わせてこれらの例を適応
- **共有**: コミュニティ向けにツールをパッケージ化することを検討

## クイックリファレンス

### 必須API関数
```python
oneenv.get_all_template_structure()  # 完全な構造を取得
oneenv.has_category(category)        # カテゴリ存在確認
oneenv.get_options(category)         # カテゴリオプション取得
oneenv.generate_template(file, selections)  # テンプレート生成
```

### CLI情報コマンド
```bash
oneenv template --structure          # 全構造を表示
oneenv template --info CATEGORY      # カテゴリ詳細
oneenv template --preview CAT OPTION # オプションプレビュー
oneenv template --structure --json   # JSON出力
```

---

**🎉 おめでとうございます！** OneEnvの情報APIを使用して強力なscaffoldingツールを作成する方法をマスターしました。これらのツールは、パッケージやプロジェクトの開発者エクスペリエンスを大幅に向上させることができます。