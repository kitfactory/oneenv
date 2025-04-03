# OneEnv 🌟　[![PyPI Downloads](https://static.pepy.tech/badge/oneenv)](https://pepy.tech/projects/oneenv)

OneEnvは、Pythonアプリケーション向けの環境変数管理・生成ツールです。  
`python-dotenv` をラップすることで、環境変数テンプレートや `.env` ファイルの取り扱いを簡素化します。

## OneEnvが解決する課題 🛠️

複数のライブラリがそれぞれ環境変数を利用する場合、各ライブラリごとに設定を管理するのは手間がかかり、エラーも発生しやすくなります。  
OneEnvは、各ライブラリで定義された環境変数テンプレートを統合し、`.env.example` を自動生成することで、手作業を大幅に軽減し、プロジェクト全体で一貫性のある設定管理を実現します。

## 特徴 🚀

- **テンプレート収集**: `@oneenv` デコレータを使用して環境変数のテンプレートを宣言できます。
- **チーム開発に最適**: 複数の小規模ライブラリが独自の環境変数を管理する必要があるマイクロサービスやモジュラー開発に最適です。
- **分散設定**: 各ライブラリが独自に環境変数を定義できるため、チーム開発での保守性とスケーラビリティが向上します。
- **自動生成された `.env.example`**: 登録されたテンプレートから統合された `.env.example` ファイルを自動生成します。
- **差分機能**: 異なるバージョンの `.env.example` ファイル間の変更点を比較できます。
- **重複キー検出**: モジュール間で重複した環境変数の定義を特定できます。
- **コマンドラインツール**: ターミナルから `oneenv template` や `oneenv diff` などのコマンドで簡単に利用できます。

## 対応環境 🖥️

- **Python**: 3.11以上
- **対応OS**: Windows, macOS, Linux

## インストール 📦

pipコマンドで簡単にインストールできます：

```bash
pip install oneenv
```

開発モードでインストールする場合は、以下のコマンドを実行してください：

```bash
pip install -e .
```

## 使い方 🚀

### テンプレート生成

登録されたテンプレートを元に `.env.example` ファイルを生成します。

```bash
oneenv template [-o OUTPUT_FILE] [-d]
```

### 差分比較

2つの `.env` ファイル間の変更点を比較するには、以下のコマンドを実行します。

```bash
oneenv diff previous.env current.env
```

### 例：`@oneenv` デコレータの使い方

以下は、`@oneenv` デコレータを用いた環境変数テンプレートの宣言例です。

```python
from oneenv import oneenv

@oneenv
def my_env_template():
    return {
        "MY_API_KEY": {
            "description": "サービスにアクセスするためのAPIキー。",
            "default": "",
            "required": True,
            "choices": []
        },
        "MODE": {
            "description": "アプリケーションモードの設定。",
            "default": "development",
            "required": False,
            "choices": ["development", "production"]
        }
    }
```

🚨 **重要な警告**: 
テンプレートモジュールは**必ずインポートする必要があります**。`@oneenv` デコレータは、インポートされたモジュールをスキャンしてデコレート済みの関数を探します。テンプレートモジュールをインポートし忘れると、**そのテンプレートは `.env.example` ファイルに含まれません**。

ディレクトリ構成例：
```
your_package/
  __init__.py      # ここでテンプレートモジュールをインポート
  template.py      # ここで@oneenvデコレータ付きの関数を定義
```

`__init__.py` の例：
```python
from . import template  # このインポートがないと、template.pyのテンプレートは発見されません
```

上記の例を参考に、コード内で `@oneenv` デコレータを使用して環境変数テンプレートを宣言できます。テンプレートを定義し、モジュールがインポートされていることを確認したら、以下のコマンドを使用してテンプレートファイルを生成できます：

```bash
oneenv template -o .env.template
```

**注:** `@oneenv` デコレータの実装では、`description` 属性だけでも十分です。他の属性（`default`、`required`、`choices`）は任意で記述できます。

### 簡単な例：シンプルなテンプレート定義

最もシンプルに利用する場合は、必須の `description` 属性だけを指定することも可能です。例えば:

```python
from oneenv import oneenv

@oneenv
def simple_config():
    return {
        "SIMPLE_VAR": {
            "description": "シンプルな環境変数です。"
        }
    }
```

## dotenvとの連携 🔄

OneEnvは [python-dotenv](https://github.com/theskumar/python-dotenv) をラップしているため、dotenvの機能をそのまま利用できます。

## テストの実行 🧪

仮想環境が有効な状態で、以下のコマンドを実行してください。

```bash
pytest tests
```

## コントリビュート 🤝

コントリビュートは大歓迎です！  
GitHub上でIssueを作成するか、Pull Requestをお送りください。

## ライセンス ⚖️

このプロジェクトはMITライセンスの下で公開されています。 