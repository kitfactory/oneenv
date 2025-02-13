# Example Usage of OneEnv Library  # oneenvライブラリの使用例

import sys  # English: Import sys for path manipulation.  # Japanese: パス操作のためにsysをインポートします。
import os   # English: Import os module.  # Japanese: osモジュールをインポートします。

from oneenv import oneenv, OneEnv, template, generate_env_example, diff, report_duplicates
# English: Import necessary functions from the oneenv library.
# Japanese: oneenvライブラリから必要な関数をインポートします。

@oneenv
def example_template():
    """
    English: Returns a dictionary of environment variable settings for the example.
    Japanese: サンプル用の環境変数設定を返す辞書を返します。
    """
    return {
        "EXAMPLE_API_KEY": {
            "description": """
                This API key is used for accessing the example service.
                This API key is used for accessing the example service.
                This API key is used for accessing the example service.
            """,      
            "default": ""
        },
        "EXAMPLE_MODE": {
            "description": "Application mode setting.",
            "default": "development",
            "required": False,
            "choices": ["development", "production"]
        }
    }

class MyLibTemplate(OneEnv):
    """
    English: Example subclass of OneEnv demonstrating template definition.
    Japanese: OneEnvを継承したテンプレート定義の使用例です。
    """
    def get_template(self) -> dict:
        """
        English: Returns a dictionary of environment variable settings for MyLib.
        Japanese: MyLib用の環境変数設定の辞書を返します。
        """
        return {
            "MYLIB_API_KEY": {
                "description": "This API key is used for accessing MyLib service.",
                "default": "",
                "required": True
            },
            "MYLIB_MODE": {
                "description": "MyLib service mode setting.",
                "default": "production",
                "required": True,
                "choices": ["development", "production"]
            }
        }

def main():
    """
    English: Main function demonstrating the usage of the oneenv library.
    Japanese: oneenvライブラリの使用例を示すメイン関数です。
    """
    # English: Generate the .env.example content using the registered templates from both
    # the @oneenv-decorated functions and OneEnv subclasses.
    # Japanese: @oneenvデコレータおよびOneEnvサブクラスから登録されたテンプレートを使用して、.env.example の内容を生成します。
    env_example_content = template()
    
    # English: Print the generated .env.example content.
    # Japanese: 生成された .env.example の内容を表示します。
    print("Generated .env.example content:")
    print(env_example_content)
    
    # English: Optionally, write the generated content to a .env.example file in the current directory.
    # Japanese: 必要に応じて、現在のディレクトリに .env.example ファイルとして書き込みます。
    output_path = os.path.join(os.getcwd(), ".env.example")
    generate_env_example(output_path)
    print(f".env.example file has been generated at: {output_path}")
    
    # English: Report any duplicate keys found in the templates.
    # Japanese: テンプレート内で重複しているキーがあれば報告します。
    report_duplicates()
    
    # English: Simulate a diff by comparing a previous version of .env.example with the current one.
    # Japanese: 過去の .env.example と現在の内容を比較し、diff の例をシミュレーションします。
    previous_example = "EXAMPLE_API_KEY=\nEXAMPLE_MODE=development\n"  # English: Simulated previous .env.example content.
                                                                        # Japanese: シミュレーションされた過去の .env.example の内容です。
    diff_result = diff(previous_example, env_example_content)
    print("Diff between previous and current .env.example content:")
    print(diff_result)

if __name__ == "__main__":
    main() 