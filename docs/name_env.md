# 通常のoneenvの使い方

oneenv.load_env(ファイル,上書き=False,)
os.environment.get(キー,デフォルト)

ただし、環境変数のため、全てのデータが同じ値になってしまう。たとえば、複数の要素に別々な設定が必要なケースでは、値が混じってしまう。

名称を付けて空間をつけられるようにします。

oneenv.load_env(ファイル, 上書き=False)
oneenv.get(キー, デフォルト)


```python
#　使用例
oneenv.env().load_dotenv("common.env")
oneenv.env("X").load_dotenv("X.env")
oneenv.env("Y").load_dotenv("Y.env")

# 共通から取得
oneenv.env().get("TIMEOUT", "30")

# 名前付き環境で取得（個別が優先、なければ共通から）
oneenv.env("X").get("API_KEY", "default-x")
```
