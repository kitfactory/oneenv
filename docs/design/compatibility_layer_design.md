# OneEnv Scaffolding形式専用設計書

## 概要

OneEnvをScaffolding形式のみに特化し、レガシー形式（直接的な環境変数辞書・groups形式）のサポートを完全に廃止。

**設計方針**: 新しいScaffolding形式のみをサポートし、シンプルで統一された体験を提供。

## サポート形式

### Scaffolding形式（唯一の形式）
```python
def database_template():
    return [
        {
            "category": "Database",
            "option": "sqlite",
            "env": {
                "DATABASE_URL": {
                    "description": "SQLiteデータベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        },
        {
            "category": "Database",
            "option": "postgres",
            "env": {
                "DATABASE_URL": {
                    "description": "PostgreSQL接続URL",
                    "default": "postgresql://user:pass@localhost:5432/dbname",
                    "required": True
                },
                "DATABASE_POOL_SIZE": {
                    "description": "コネクションプール最大サイズ",
                    "default": "10",
                    "required": False
                }
            }
        }
    ]
```

## 形式検証メカニズム

### validate_scaffolding_format() 仕様

```python
def validate_scaffolding_format(template_data: Any) -> bool:
    """
    Scaffolding形式のテンプレートデータを検証
    
    Args:
        template_data: テンプレート関数から返されたデータ
        
    Returns:
        検証成功時True
        
    Raises:
        ValueError: 不正な形式の場合
    """
```

### 検証ロジック

```python
def validate_scaffolding_format(template_data: Any) -> bool:
    """Scaffolding形式の厳密な検証"""
    
    # 1. リスト形式必須
    if not isinstance(template_data, list):
        raise ValueError("Template must be a list of options")
    
    # 2. 空リスト禁止
    if not template_data:
        raise ValueError("Template cannot be empty")
    
    # 3. 各要素の検証
    category_option_pairs = set()
    
    for i, item in enumerate(template_data):
        # 辞書形式必須
        if not isinstance(item, dict):
            raise ValueError(f"Option {i}: Must be a dictionary")
        
        # 必須キー確認
        required_keys = {"category", "option", "env"}
        missing_keys = required_keys - set(item.keys())
        if missing_keys:
            raise ValueError(f"Option {i}: Missing required keys: {missing_keys}")
        
        # カテゴリ/オプション検証
        category = item["category"]
        option = item["option"]
        
        if not isinstance(category, str) or not category.strip():
            raise ValueError(f"Option {i}: category must be non-empty string")
        
        if not isinstance(option, str) or not option.strip():
            raise ValueError(f"Option {i}: option must be non-empty string")
        
        # 一意性検証
        pair = (category.strip(), option.strip())
        if pair in category_option_pairs:
            raise ValueError(f"Option {i}: Duplicate category/option pair: {category}/{option}")
        category_option_pairs.add(pair)
        
        # env検証
        env_data = item["env"]
        if not isinstance(env_data, dict) or not env_data:
            raise ValueError(f"Option {i}: env must be non-empty dictionary")
        
        # env内の各環境変数検証
        for var_name, var_config in env_data.items():
            if not isinstance(var_name, str) or not var_name.strip():
                raise ValueError(f"Option {i}: Environment variable name must be non-empty string")
            
            if not isinstance(var_config, dict):
                raise ValueError(f"Option {i}: Environment variable {var_name} config must be dictionary")
            
            # 必須フィールド確認
            if "description" not in var_config:
                raise ValueError(f"Option {i}: Environment variable {var_name} missing description")
    
    return True
```

## シンプルなテンプレート処理システム

### Scaffolding専用処理

```python
class ScaffoldingTemplateProcessor:
    """
    Scaffolding形式専用のテンプレート処理
    """
    
    def __init__(self):
        self.env_options: List[EnvOption] = []
    
    def add_template(self, func_name: str, template_data: List[Dict[str, Any]]):
        """
        Scaffolding形式テンプレートを追加
        """
        # 形式検証
        validate_scaffolding_format(template_data)
        
        # EnvOptionリストに変換
        options = scaffolding_template_function_to_env_options(func_name, template_data)
        self.env_options.extend(options)
    
    def get_template_structure(self) -> Dict[str, List[str]]:
        """
        カテゴリ別オプション構造を返却
        """
        structure = {}
        
        for option in self.env_options:
            category = option.category
            if category not in structure:
                structure[category] = []
            
            if option.option not in structure[category]:
                structure[category].append(option.option)
        
        return structure
    
    def has_category(self, category: str) -> bool:
        """
        指定カテゴリの存在確認
        """
        return any(option.category == category for option in self.env_options)
    
    def get_options(self, category: str) -> List[str]:
        """
        カテゴリ内の全オプション取得
        """
        options = []
        for option in self.env_options:
            if option.category == category and option.option not in options:
                options.append(option.option)
        return options
    
    def generate_by_selection(self, generation_range: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        選択範囲に基づいて環境変数を生成
        """
        selected_vars = {}
        
        for selection in generation_range:
            category = selection["category"]
            option = selection.get("option")  # None = 全オプション
            
            for env_option in self.env_options:
                if env_option.category == category:
                    if option is None or env_option.option == option:
                        # 環境変数追加
                        for var_name, var_config in env_option.env.items():
                            selected_vars[var_name] = env_var_config_to_dict(var_config)
        
        return selected_vars
```

## シンプルなAPI設計

### 統一されたAPI

```python
# Scaffolding形式専用のシンプルなAPI

def get_all_template_structure() -> Dict[str, List[str]]:
    """
    全テンプレート構造をカテゴリ別オプション一覧で返却
    """
    processor = ScaffoldingTemplateProcessor()
    # 全テンプレートを収集
    load_all_scaffolding_templates(processor)
    return processor.get_template_structure()

def has_category(category: str) -> bool:
    """
    指定カテゴリの存在確認
    """
    processor = ScaffoldingTemplateProcessor()
    load_all_scaffolding_templates(processor)
    return processor.has_category(category)

def get_options(category: str) -> List[str]:
    """
    カテゴリ内の全オプション取得
    """
    processor = ScaffoldingTemplateProcessor()
    load_all_scaffolding_templates(processor)
    return processor.get_options(category)

def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str:
    """
    選択的テンプレート生成
    """
    processor = ScaffoldingTemplateProcessor()
    load_all_scaffolding_templates(processor)
    
    selected_vars = processor.generate_by_selection(generation_range)
    
    # .envファイル形式で出力
    env_content = generate_env_file_content(selected_vars)
    
    if dest:
        with open(dest, 'w') as f:
            f.write(env_content)
    
    return env_content

def load_all_scaffolding_templates(processor: ScaffoldingTemplateProcessor):
    """
    インストールされた全パッケージからScaffolding形式テンプレートを読み込み
    """
    # entry-pointsからテンプレート関数を発見
    import pkg_resources
    
    for entry_point in pkg_resources.iter_entry_points('oneenv.templates'):
        try:
            template_func = entry_point.load()
            template_data = template_func()
            
            # Scaffolding形式のみ受け入れ
            validate_scaffolding_format(template_data)
            processor.add_template(entry_point.name, template_data)
            
        except Exception as e:
            # 不正な形式は無視（ログ出力）
            print(f"Warning: Skipping invalid template {entry_point.name}: {e}")
```

## エラーハンドリング

### 検証エラー

```python
class ScaffoldingFormatError(ValueError):
    """Scaffolding形式エラー"""
    pass

def safe_template_loading():
    """
    安全なテンプレート読み込み
    不正な形式のテンプレートはスキップ
    """
    valid_templates = []
    errors = []
    
    for entry_point in pkg_resources.iter_entry_points('oneenv.templates'):
        try:
            template_func = entry_point.load()
            template_data = template_func()
            
            # 検証
            validate_scaffolding_format(template_data)
            valid_templates.append((entry_point.name, template_data))
            
        except Exception as e:
            errors.append(f"Template {entry_point.name}: {str(e)}")
    
    return valid_templates, errors
```

## 移行戦略

### 段階的移行

1. **Phase 1**: Scaffolding形式の新API追加
2. **Phase 2**: 既存API（groups/legacy）の非推奨化
3. **Phase 3**: 既存APIの削除警告
4. **Phase 4**: メジャーバージョンアップでScaffolding専用化

### 移行支援

```python
def convert_legacy_to_scaffolding_guide():
    """
    レガシー形式からScaffolding形式への変換ガイド生成
    """
    guide = """
    # レガシー形式 → Scaffolding形式 変換ガイド
    
    ## Before (Groups形式):
    @oneenv
    def database_template():
        return {
            "groups": {
                "Database": {
                    "DATABASE_URL": {
                        "description": "データベース接続URL",
                        "default": "sqlite:///app.db"
                    }
                }
            }
        }
    
    ## After (Scaffolding形式):
    def database_template():
        return [
            {
                "category": "Database",
                "option": "sqlite",
                "env": {
                    "DATABASE_URL": {
                        "description": "SQLiteデータベース接続URL", 
                        "default": "sqlite:///app.db"
                    }
                }
            }
        ]
    """
    return guide
```

## テスト戦略

### 主要テスト

```python
def test_scaffolding_format_validation():
    """Scaffolding形式検証テスト"""

def test_template_processing():
    """テンプレート処理テスト"""

def test_api_functions():
    """API関数テスト"""

def test_error_handling():
    """エラーハンドリングテスト"""
```

## まとめ

**簡素化された設計により:**

1. **統一性**: Scaffolding形式のみでシンプル
2. **明確性**: category/optionによる明確な構造
3. **拡張性**: 新しいカテゴリ/オプションを簡単に追加
4. **保守性**: 複雑な互換性レイヤーが不要

既存のgroups/legacy形式を廃止し、新しいScaffolding形式に特化することで、より保守しやすく使いやすいシステムになります。