# Scafolding

たとえばRAGのような複数技術に関する設定を管理する設定を記載する必要がある場合があります。

RAG, VectorStore, KeywordSearchといった技術からなります。そこでインストールされている環境から、ユーザーに適切にパッケージを選択させ、必要な情報に絞った.envファイルを作成したい要望があります。

つまり、oneenvでインストールされているパッケージの環境情報を取得する際に、あわせてカテゴリ情報も取得して、そのカテゴリ情報にあわせてインストールされているパッケージを把握するのです。

例えばVectorStoreにChromaを使用したいが、Weaviateもインストールされている場合、VectorStoreをどちらにするか選択してもらう必要があります。

たとえば、下記のように。

```bash
Rag機能を使用しますか？ > (n/Y)

使用するVectorStoreを選択してください。
    [ ] Chroma
    [ ] Weaviate

```

そのため、テンプレートから返却されるテンプレート情報に、もう一段深くしたいと思います。

旧型式から新しいデータ形式に変更したいと思います

```python
# mypackage/templates.py
def database_template():
    return [
        {
            "category": "Database",　//従来のグループに相当
            "option": "sqlite", // 新規追加。有効時のみ下記の環境変数が有効に
            "env": {
                "DATABASE_URL": {
                    "description": "データベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                },
                // 他の変数
            }
        }
    ]
```

`pyproject.toml`に登録:
```toml
[project.entry-points."oneenv.templates"]
database = "mypackage.templates:database_template"
```

## テンプレート返却関数

scafoldするパッケージに情報を提供する関数をパッケージから提供する。


### テンプレートの全体構造

各パッケージのテンプレート関数から返却された、全てのテンプレート情報を統合して返却する。
oneenv.get_all_template_structure()


### カテゴリの把握

現在のテンプレート状況に指定されたカテゴリがあるか返却する。
oneenv.has_category(カテゴリ名)

### オプションの把握

指定されたカテゴリ内の全てのカテゴリを返却する。ない場合は[]
oneenv.get_options(カテゴリ名)


### 選択されたカテゴリ、オプションを用いてテンプレート .envファイルを作成

選択されたカテゴリ、オプションを用いてテンプレート .envファイルを作成する、カテゴリ無指定時は全てのカテゴリ、全てのオプション、オプションが無指定時はそのカテゴリ内の全てのオプションを使ってファイルを生成する。

generation_range = {
    [
        "category": "vectorstore",
        "option" : "chroma",
    ],
    [
        "category": "rag",
    ]
}
dest = "....env"

oneenv.generate_template(dest, generation_range)
