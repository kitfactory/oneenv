# Phase 2.1: 生成エンジン詳細仕様書

## 概要

Phase 1で実装済みの基本的なScaffolding APIを基に、生成エンジンの詳細仕様を策定し、実装の完成度を高める。

## 現在の実装状況

### ✅ 実装済み機能 (Phase 1)

1. **基本API**
   - `get_all_template_structure()` - カテゴリ別オプション構造取得
   - `has_category(category)` - カテゴリ存在確認
   - `get_options(category)` - カテゴリ内全オプション取得
   - `generate_template(dest, generation_range)` - 選択的テンプレート生成

2. **コア機能**
   - `ScaffoldingTemplateProcessor` - 新形式テンプレート処理
   - `generate_env_file_content()` - 重要度別出力生成
   - Scaffolding形式検証とエラーハンドリング

3. **テスト**
   - 27個のテストケース（100%成功）
   - 引数検証、エラーハンドリング、ファイル出力テスト

## Phase 2.1で実装・改善する項目

### 🎯 2.1.1: 生成ロジックの最適化

#### 現在の課題
- `generate_template()`は基本実装のみ
- 複雑な選択パターンへの対応不足
- パフォーマンス最適化の余地

#### 改善項目

1. **高度な選択パターン対応**
   ```python
   # 現在サポート済み
   generation_range = [
       {"category": "Database", "option": "postgres"},  # 特定オプション
       {"category": "VectorStore"}                      # 全オプション
   ]
   
   # Phase 2.1で追加
   generation_range = [
       {"category": "Database", "exclude": ["mysql"]},      # 除外指定
       {"category": "VectorStore", "filter": "required"},   # 必須のみ
       {"category": "Cache", "importance": "critical"}      # 重要度指定
   ]
   ```

2. **条件付き生成ロジック**
   - 重要度フィルタリング
   - 必須/任意フィルタリング
   - 除外パターン対応

3. **パフォーマンス最適化**
   - テンプレート読み込みのキャッシュ化
   - 大量オプション処理の最適化

### 🎯 2.1.2: 従来システムとの統合強化

#### 統合戦略

1. **レガシー形式との相互運用**
   ```python
   # 既存@oneenvデコレータとの混在
   @oneenv
   def legacy_template():
       return {"VAR": {"description": "..."}}
   
   # 新Scaffolding形式
   def scaffolding_template():
       return [{"category": "...", "option": "...", "env": {...}}]
   ```

2. **ハイブリッド生成**
   - レガシー + Scaffolding形式の混在出力
   - 重複変数の適切な処理
   - ソース表示の統一

### 🎯 2.1.3: 出力形式の高度化

#### 現在の出力形式
```bash
# ========== CRITICAL: Essential Settings ==========

# ----- Database (postgres) -----

# PostgreSQL connection URL
# Required
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

#### Phase 2.1での拡張

1. **カスタマイズ可能な出力形式**
   ```python
   generate_template(
       dest="",
       generation_range=[...],
       format_options={
           "include_sources": True,     # ソース情報表示
           "include_examples": True,    # 使用例表示
           "group_by": "importance",    # グループ化基準
           "locale": "ja"               # ロケール指定
       }
   )
   ```

2. **多言語対応の出力**
   - 日本語/英語の重要度ヘッダー
   - ロケール自動検出との連携

3. **使用例と説明の充実**
   ```bash
   # データベース接続URL
   # 例: postgresql://user:pass@localhost:5432/dbname
   # 例: sqlite:///path/to/database.db
   # Required
   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
   ```

### 🎯 2.1.4: エラーハンドリングとバリデーション強化

#### 現在の検証レベル
- 基本的な引数検証
- Scaffolding形式の構造検証

#### Phase 2.1での強化

1. **高度なバリデーション**
   ```python
   # 循環依存の検出
   # 矛盾する設定の検出
   # 不完全な選択の警告
   ```

2. **詳細なエラーメッセージ**
   ```python
   # 現在: "Category not found"
   # 改善: "Category 'InvalidCategory' not found. Available categories: Database, VectorStore, Cache"
   ```

3. **警告システム**
   - 非推奨オプションの警告
   - 不完全な設定の提案

## 実装優先順位

### 🥇 高優先度 (Phase 2.1 必須)
1. **高度な選択パターン対応** - 基本的な除外/フィルタ機能
2. **従来システムとの統合** - レガシー形式との混在対応
3. **エラーメッセージ改善** - ユーザーフレンドリーなエラー表示

### 🥈 中優先度 (Phase 2.1 推奨)
1. **出力形式のカスタマイズ** - format_optionsパラメータ
2. **パフォーマンス最適化** - キャッシュメカニズム
3. **多言語対応強化** - 日本語ローカライゼーション

### 🥉 低優先度 (Phase 3以降)
1. **使用例の自動生成** - 高度なドキュメント機能
2. **設定の妥当性チェック** - 複雑な依存関係検証

## API設計案

### 拡張された`generate_template()`

```python
def generate_template(
    dest: str,
    generation_range: List[Dict[str, Any]], 
    format_options: Optional[Dict[str, Any]] = None,
    validation_level: str = "standard"
) -> str:
    """
    選択的テンプレート生成（Phase 2.1拡張版）
    
    Args:
        dest: 出力先ファイルパス
        generation_range: 生成範囲指定
            [
                {"category": "Database", "option": "postgres"},
                {"category": "Cache", "exclude": ["redis"]},
                {"category": "VectorStore", "importance": "critical"}
            ]
        format_options: 出力形式オプション
            {
                "include_sources": bool,
                "include_examples": bool,
                "group_by": "importance" | "category",
                "locale": "en" | "ja"
            }
        validation_level: "strict" | "standard" | "permissive"
    
    Returns:
        生成された.envファイル内容
    """
```

### 新しいヘルパー関数

```python
def validate_generation_range(generation_range: List[Dict[str, Any]]) -> List[str]:
    """生成範囲の詳細バリデーション"""

def merge_legacy_and_scaffolding(
    legacy_templates: Dict[str, Any],
    scaffolding_selection: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """レガシーとScaffolding形式の統合"""

def optimize_template_loading() -> None:
    """テンプレート読み込みの最適化"""
```

## 成功基準

### 機能面
- ✅ 基本的な除外/フィルタ機能の動作
- ✅ レガシー形式との混在出力
- ✅ 改善されたエラーメッセージ

### パフォーマンス面
- ✅ 1000個のオプションを1秒以内で処理
- ✅ テンプレート再読み込みの最適化

### ユーザビリティ面
- ✅ 直感的なエラーメッセージ
- ✅ 実用的な警告システム

## 次のステップ

1. **ユーザー確認**: この仕様に対するフィードバック取得
2. **実装計画**: 優先順位に従った段階的実装
3. **テスト拡張**: 新機能に対応したテストケース追加

---

**注意**: この仕様は既存のPhase 1実装を基に、実用性とパフォーマンスを重視した拡張案です。