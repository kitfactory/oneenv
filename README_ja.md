# OneEnv 🌟

OneEnvは、Pythonアプリケーション向けの環境変数管理・生成ツールです。  
`python-dotenv` をラップすることで、環境変数テンプレートや `.env` ファイルの取り扱いを簡素化します。

## OneEnvが解決する課題 🛠️

複数のライブラリがそれぞれ環境変数を利用する場合、各ライブラリごとに設定を管理するのは手間がかかり、エラーも発生しやすくなります。  
OneEnvは、各ライブラリで定義された環境変数テンプレートを統合し、`.env.example` を自動生成することで、手作業を大幅に軽減し、プロジェクト全体で一貫性のある設定管理を実現します。

## 特徴 🚀

- **テンプレート収集**: `@oneenv` デコレータを使用して環境変数のテンプレートを宣言できます。
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
oneenv template [-o OUTPUT_FILE]
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

上記の例を参考に、コード内でデコレータを利用して環境変数テンプレートを自動登録できます。

**注:** `description` 属性だけでも十分です。他の属性（`default`、`required`、`choices`）は任意で記述できます。

### 簡単な例：`description` 属性のみの場合

最もシンプルに利用する場合は、`description` 属性だけを指定することも可能です。例えば:

```python
from oneenv import oneenv

@oneenv
def minimal_template():
    return {
        "SIMPLE_VAR": {
            "description": "シンプルな環境変数です。"
        }
    }
```

この簡単な例は、利用の容易さを強調しており、`description` 属性だけでも十分に動作します。さらに、OneEnvは `python-dotenv` のラッパーであるため、dotenv としても環境変数の読み込みに利用できます。

## dotenvとの連携 🔄

OneEnvは、環境変数テンプレートの自動生成だけでなく、[python-dotenv](https://github.com/theskumar/python-dotenv) をラップすることで、環境変数を簡単に読み込むことも可能です。

### 例：OneEnvを使って環境変数を読み込む

OneEnvを利用すれば、`.env` ファイルから環境変数を読み込み、アプリケーションに反映させることができます。以下はその例です：

```python
from oneenv import load_dotenv, dotenv_values

# 環境変数を現在のプロセスに読み込みます
load_dotenv()

# または、辞書形式で取得することも可能です
env_vars = dotenv_values(".env")
print(env_vars)
```

この連携により、環境変数の管理を一元化しながら、python-dotenvの機能をすべて活用できます。

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