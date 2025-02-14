import difflib
import sys
import os
import pkgutil
import importlib
from abc import ABC, abstractmethod

from dotenv import load_dotenv as dotenv_load_dotenv  # English: Import load_dotenv from python-dotenv.
                                                    # Japanese: python-dotenvからload_dotenvをインポートします。
from dotenv import dotenv_values as _dotenv_values  # English: Import dotenv_values from python-dotenv.
                                                   # Japanese: python-dotenvからdotenv_valuesをインポートします。

# Global registry for template functions  # English: Global registry for storing functions decorated with @oneenv.
                                           # Japanese: @oneenvデコレータが付与された関数を格納するグローバルレジストリ。
_TEMPLATE_REGISTRY = []

def oneenv(func):
    """
    English: Decorator that registers a function providing environment variable templates.
    Input:
      - func: The function that returns a dictionary of environment variable settings.
    Output:
      - The original function with the side-effect of being registered.
    Japanese: 環境変数テンプレートを提供する関数を登録するデコレータです。
    入力:
      - func: 環境変数設定の辞書を返す関数。
    出力:
      - 登録の副作用を持ち、元の関数を返します。
    """
    # Register the function in the template registry  # English: Register the function in the global registry.
                                                       # Japanese: グローバルレジストリに関数を登録します。
    _TEMPLATE_REGISTRY.append(func)
    return func

class OneEnv(ABC):
    """
    English: Abstract base class for defining environment variable templates.
    Japanese: 環境変数テンプレートを定義するための抽象基本クラスです。
    """
    @abstractmethod
    def get_template(self) -> dict:
        """
        English: Returns the template dictionary for environment variables.
        Japanese: 環境変数のテンプレート辞書を返します。
        """
        pass

def collect_templates():
    """
    English: Collects and combines environment variable templates from registered functions.
    Returns a dictionary mapping keys to their configuration and list of sources (function names).
    Output format:
       { key: { "config": { ... }, "sources": [func_name, ...] }, ... }
    Japanese: 登録された関数から環境変数テンプレートを収集し、統合します。
    各キーに対して、その設定情報と定義元の関数名リストを含む辞書を返します。
    出力形式:
       { key: { "config": { ... }, "sources": [関数名, ...] }, ... }
    """
    templates = {}  # English: Dictionary to hold combined templates.
                    # Japanese: 統合されたテンプレートを格納する辞書。
    for func in _TEMPLATE_REGISTRY:
        # English: Call each registered function to obtain its template dictionary.
        # Japanese: 登録されている各関数を呼び出して、テンプレート辞書を取得します。
        template_dict = func()
        for key, config in template_dict.items():
            # English: Verify that the 'description' field is present.
            # Japanese: 'description'フィールドが存在するか確認します。
            if "description" not in config:
                raise ValueError(f"Missing 'description' for key {key} in {func.__name__}")
            if key in templates:
                # Append the function name only if it hasn't been added already.
                # 重複していなければ定義元関数名リストに追加します。
                if func.__name__ not in templates[key]["sources"]:
                    templates[key]["sources"].append(func.__name__)
            else:
                # English: Add a new key with its configuration and source.
                # Japanese: 新規キーとして設定情報と定義元関数を追加します。
                templates[key] = {"config": config, "sources": [func.__name__]}
    return templates

def report_duplicates():
    """
    English: Reports duplicate environment variable keys across multiple templates.
             Prints warnings if duplicate keys are found.
    Japanese: 複数のテンプレート間で重複している環境変数のキーを検出し、警告を出力します。
    """
    templates = collect_templates()
    # English: Iterate over each template to check for duplicates.
    # Japanese: 各テンプレートについて重複キーがないか確認します。
    for key, info in templates.items():
        if len(info["sources"]) > 1:
            # English: Print warning for duplicate key.
            # Japanese: 重複するキーの警告を出力します。
            print(f"Warning: Duplicate key '{key}' defined in {', '.join(info['sources'])}")

def template(debug=False):
    """
    English: Generates the text content of the .env.example file based on collected templates.
             Each variable includes its description, source, and default value.
    Output:
      - A string with the content for .env.example.
    Japanese: 収集したテンプレートに基づいて、.env.exampleファイルのテキスト内容を生成します。
             各環境変数は説明、定義元の関数、既定値を含みます。
    出力:
      - .env.example用の内容を持つ文字列を返します。
    """
    if debug:
        print("\nDiscovering modules and templates...")
    
    # Import all modules to discover @oneenv decorated functions
    imported_modules = import_templates(debug)
    if debug:
        print(f"\nDiscovered non-standard modules: {len(imported_modules)}")
        for module in imported_modules:
            if not module.startswith('_') and not any(module.startswith(std) for std in ['os', 'sys', 'importlib', 'pkgutil']):
                print(f"  - {module}")
    
    templates_data = collect_templates()
    if debug:
        print(f"\nDiscovered @oneenv decorated functions: {len(_TEMPLATE_REGISTRY)}")
        for func in _TEMPLATE_REGISTRY:
            print(f"  - {func.__name__}")
        print("")

    # Group the variables by their sorted tuple of sources
    groups = {}
    for key, info in templates_data.items():
        group_key = tuple(sorted(info["sources"]))
        groups.setdefault(group_key, []).append((key, info["config"]))

    lines = []
    # Header indicating auto-generation
    lines.append("# Auto-generated by OneEnv")
    lines.append("")

    # Process each group (same defined source)
    for sources, items in groups.items():
        sources_str = ", ".join(sources)
        lines.append(f"# (Defined in: {sources_str})")
        # Process each variable in the group
        for key, config in items:
            description = config.get("description", "")
            default_value = config.get("default", "")
            required_value = config.get("required", False)
            choices_value = config.get("choices", None)
            # Print description lines (English only)
            for line in description.splitlines():
                stripped_line = line.strip()
                if stripped_line:
                    lines.append(f"# {stripped_line}")
            # If the variable is required, output a comment line for it
            if required_value:
                lines.append("# Required")
            # If there are choices defined, output them as well
            if choices_value:
                lines.append(f"# Choices: {', '.join(choices_value)}")
            # Print the variable assignment
            lines.append(f"{key}={default_value}")
            lines.append("")
        lines.append("")
    return "\n".join(lines)

def diff(previous_text, current_text):
    """
    English: Compares two .env.example texts and returns a diff string showing additions and modifications.
             For a modified line, displays the change in the format: "~ old_line → new_line".
    Input:
      - previous_text: The previous .env.example content.
      - current_text: The current .env.example content.
    Output:
      - A string representing the differences.
    Japanese: 2つの.env.exampleファイルのテキストを比較し、追加および変更箇所を示すdiff文字列を返します。
             変更箇所は "~ 古い行 → 新しい行" の形式で表示されます。
    入力:
      - previous_text: 以前の.env.exampleの内容
      - current_text: 現在の.env.exampleの内容
    出力:
      - 差分を表す文字列を返します。
    """
    previous_lines = previous_text.splitlines()
    current_lines = current_text.splitlines()
    differ = difflib.Differ()
    diff_list = list(differ.compare(previous_lines, current_lines))
    result_lines = []
    i = 0
    # English: Iterate over the diff list to process removals and additions.
    # Japanese: diffリストを反復し、削除と追加の行を処理します。
    while i < len(diff_list):
        line = diff_list[i]
        if line.startswith("- "):
            # English: Check if the next line is an addition to combine as a modification.
            # Japanese: 次の行が追加であれば、変更として結合します。
            if i + 1 < len(diff_list) and diff_list[i + 1].startswith("+ "):
                old_line = line[2:]
                new_line = diff_list[i + 1][2:]
                if not old_line.startswith("#") and "=" in old_line:
                    result_lines.append(f"~ {old_line} → {new_line}")
                    i += 2
                    continue
            result_lines.append(f"- {line[2:]}")
        elif line.startswith("+ "):
            result_lines.append(f"+ {line[2:]}")
        i += 1
    return "\n".join(result_lines)

def generate_env_example(output_path):
    """
    English: Generates the .env.example file at the specified output path using the current templates.
    Input:
      - output_path: The file path where the .env.example should be written.
    Japanese: 現在のテンプレートを用いて、指定された出力パスに.env.exampleファイルを生成します。
    入力:
      - output_path: .env.exampleを書き込むファイルパス
    """
    content = template()
    # English: Write the generated content to the specified file.
    # Japanese: 生成された内容を指定されたファイルに書き込みます。
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(content)

def load_dotenv(dotenv_path=None, override=False):
    """
    English: Loads environment variables from a .env file using python-dotenv.
    Input:
      - dotenv_path: The path to the .env file (optional).
      - override: Whether to override existing environment variables (default False).
    Output:
      - Returns a boolean indicating success.
    Japanese: python-dotenvを使用して、.envファイルから環境変数を読み込みます。
    入力:
      - dotenv_path: .envファイルへのパス（オプション）
      - override: 既存の環境変数を上書きするかどうか（デフォルトはFalse）
    出力:
      - 成功を示すブール値を返します。
    """
    return dotenv_load_dotenv(dotenv_path=dotenv_path, override=override)

def dotenv_values(dotenv_path=None, encoding='utf-8'):
    """
    English: Returns the environment variables from a .env file as a dictionary using python-dotenv.
    Input:
      - dotenv_path: The path to the .env file (optional).
      - encoding: The encoding for reading the .env file (default 'utf-8').
    Output:
      - A dictionary containing the environment variables.
    Japanese: python-dotenvを使用して、.envファイルから環境変数を辞書形式で返します。
    入力:
      - dotenv_path: .envファイルへのパス（オプション）
      - encoding: .envファイルを読み込む際のエンコーディング（デフォルトは'utf-8'）
    出力:
      - 環境変数が格納された辞書を返します。
    """
    return _dotenv_values(dotenv_path=dotenv_path, encoding=encoding)

def set_key(dotenv_path, key_to_set, value_to_set):
    """
    English: Sets or updates an environment variable in the specified .env file.
    Input:
      - dotenv_path: The path to the .env file.
      - key_to_set: The environment variable name to set.
      - value_to_set: The value to assign to the environment variable.
    Japanese: 指定された.envファイルに対して、環境変数の値を設定または更新します。
    入力:
      - dotenv_path: .envファイルへのパス
      - key_to_set: 設定する環境変数の名前
      - value_to_set: 環境変数に割り当てる値
    """
    try:
        # English: Attempt to read the existing .env file.
        # Japanese: 既存の.envファイルを読み込もうと試みます。
        with open(dotenv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        # English: If not found, start with an empty list.
        # Japanese: ファイルが見つからない場合、空のリストから開始します。
        lines = []
    key_prefix = f"{key_to_set}="
    found = False
    new_lines = []
    # English: Iterate through each line and update the target key if it exists.
    # Japanese: 各行を処理し、対象のキーが存在する場合は更新します。
    for line in lines:
        if line.startswith(key_prefix):
            new_lines.append(f"{key_to_set}={value_to_set}\n")
            found = True
        else:
            new_lines.append(line)
    if not found:
        # English: If key is not present, append it.
        # Japanese: キーが存在しない場合、新たに追加します。
        new_lines.append(f"{key_to_set}={value_to_set}\n")
    # English: Write the updated content back to the .env file.
    # Japanese: 更新された内容を.envファイルに書き戻します。
    with open(dotenv_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

def unset_key(dotenv_path, key_to_unset):
    """
    English: Removes an environment variable from the specified .env file.
    Input:
      - dotenv_path: The path to the .env file.
      - key_to_unset: The environment variable name to remove.
    Japanese: 指定された.envファイルから環境変数を削除します。
    入力:
      - dotenv_path: .envファイルへのパス
      - key_to_unset: 削除する環境変数の名前
    """
    try:
        # English: Attempt to read the existing .env file.
        # Japanese: 既存の.envファイルを読み込もうと試みます。
        with open(dotenv_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        # English: If the file is not found, there is nothing to remove.
        # Japanese: ファイルが存在しなければ、削除する内容はありません。
        lines = []
    new_lines = []
    key_prefix = f"{key_to_unset}="
    # English: Exclude the line corresponding to the specified key.
    # Japanese: 指定されたキーに該当する行を除外します。
    for line in lines:
        if not line.startswith(key_prefix):
            new_lines.append(line)
    # English: Write the filtered content back to the .env file.
    # Japanese: フィルタリングされた内容を.envファイルに書き戻します。
    with open(dotenv_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

# 新規: sys.path 内のモジュールを自動探索・インポートする仕組み
# New: Automatically discover and import modules in sys.path to trigger the @oneenv decorators.
def import_templates(debug=False):
    """
    English: Automatically discovers and imports modules within directories under the current working directory in sys.path.
    This triggers the registration of all functions decorated with @oneenv.
    Japanese: 現在の作業ディレクトリ以下にあるsys.path上のディレクトリ内のモジュールを自動探索・インポートします。
    これにより、@oneenvデコレータが付与されたすべての関数が登録されることを保証します。
    Output:
      - A list of successfully imported module names.
      - 登録に成功したモジュール名のリストを返します。
    """

    cwd = os.getcwd()  # English: Get the current working directory.
                      # Japanese: 現在の作業ディレクトリを取得します。
    imported_modules = []
    for path_item in sys.path:
        abs_path = os.path.abspath(path_item)
        if not os.path.isdir(abs_path):
            continue
        # Restrict search to directories under the current working directory to avoid system libraries.
        # 現在の作業ディレクトリ下にあるディレクトリに限定して探索し、システムライブラリを除外します。
        if not abs_path.startswith(cwd):
            continue
        for finder, modname, ispkg in pkgutil.iter_modules([abs_path]):
            try:
                importlib.import_module(modname)
                imported_modules.append(modname)
                if debug:
                    print(f"Imported module: {modname}")
            except Exception as e:
                print(f"OneEnv import_templates: Could not import module {modname} from {abs_path}: {e}")
    return imported_modules

def import_all_modules(package, debug=False):
    """
    English: Import all modules in the given package.
    Japanese: 指定されたパッケージ内のすべてのモジュールをインポートします。
    """
    import pkgutil
    import importlib
    imported = []
    if hasattr(package, '__path__'):
        for finder, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
            try:
                importlib.import_module(module_name)
                imported.append(module_name)
                if debug:
                    print(f"Imported module: {module_name}")
            except Exception as e:
                print(f"Error importing module {module_name}: {e}")
    return imported
 