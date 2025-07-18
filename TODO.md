# OneEnv Scaffolding System Implementation Plan

## 概要

OneEnvにスキャフォールディング機能を追加し、ユーザーがインタラクティブにパッケージを選択して最適化された`.env`ファイルを生成できるようにする。

## 要求仕様（docs/scaffolding.mdより）

### 目標
- RAG/VectorStore/KeywordSearchなど複数技術の組み合わせに対応
- ユーザーがインタラクティブにパッケージを選択
- 選択された構成のみの.envファイル生成

### 新テンプレート形式
```python
def database_template():
    return [
        {
            "category": "Database",  # グループ相当
            "option": "sqlite",     # 選択可能オプション
            "env": {
                "DATABASE_URL": {
                    "description": "データベース接続URL",
                    "default": "sqlite:///app.db",
                    "required": True
                }
            }
        }
    ]
```

### 新API要件
- `oneenv.get_all_template_structure()` - 全テンプレート構造取得
- `oneenv.has_category(category)` - カテゴリ存在確認
- `oneenv.get_options(category)` - カテゴリ内オプション取得
- `oneenv.generate_template(dest, generation_range)` - 選択的テンプレート生成

## 実装計画

### Phase 1: 基盤設計・データモデル拡張 🏗️

#### 1.1 簡素化されたデータモデル設計
- [x] **設計書作成**: 簡素化された`EnvOption` Pydanticモデル仕様書
- [x] **👤 ユーザー確認**: データモデル設計レビュー・承認 ✅
- [x] `EnvOption` Pydanticモデル実装（category/option/env構造のみ） ✅
- [x] **設計書作成**: Scaffolding形式専用設計書（レガシー廃止） ✅
- [x] **👤 ユーザー確認**: 互換性戦略レビュー・承認 ✅
- [x] Scaffolding形式検証メカニズム実装 ✅

#### 1.2 コア機能実装
- [x] **設計書作成**: 新API仕様書（`get_all_template_structure()`等） ✅
- [x] **👤 ユーザー確認**: API設計レビュー・承認 ✅
- [x] `get_all_template_structure()` 実装 ✅
- [x] `has_category()` 実装 ✅
- [x] `get_options()` 実装 ✅
- [x] `generate_template()` 実装 ✅
- [x] 新形式テンプレート収集システム実装 ✅
- [x] **重要度による出力分類**: `generate_env_file_content()`を重要度（critical/important/optional）とカテゴリ別に分類するよう修正 ✅
- [x] **包括的テストスイート**: 27個のテストケース作成（全て成功） ✅
- [x] **👤 ユーザー確認**: 実装結果デモ・動作確認 ✅

**推定期間**: 3-4日（ユーザー確認時間含む）

### Phase 2: 選択的テンプレート生成システム 🎯

#### 2.1 生成エンジン実装
- [x] **設計書作成**: `generate_template()` 詳細仕様書 ✅
- [x] **👤 ユーザー確認**: 生成ロジック設計レビュー・承認 ✅
- [x] `generate_template()` コア実装 ✅
- [x] カテゴリ/オプション選択ロジック実装 ✅
- [x] 従来テンプレート生成との統合 ✅
- [x] 出力形式の最適化 ✅
- [x] **👤 ユーザー確認**: 生成結果サンプル確認・調整 ✅

**推定期間**: 2-3日（ユーザー確認時間含む）

### Phase 3: CLI統合・情報提供API 🖥️

#### 3.1 `oneenv template`サブコマンド拡張
- [x] **設計書作成**: `oneenv template`情報提供モード詳細仕様書 ✅
- [x] **👤 ユーザー確認**: CLI拡張設計レビュー・承認 ✅
- [x] `oneenv template --structure` - 利用可能なカテゴリ/オプション構造の表示 ✅
- [x] `oneenv template --info <category>` - カテゴリ詳細情報の表示 ✅
- [x] `oneenv template --preview <category> <option>` - 特定オプションのプレビュー ✅
- [x] **👤 ユーザー確認**: CLI機能動作確認・フィードバック ✅

#### 3.2 プログラマティックAPI強化
- [x] **設計書作成**: パッケージ側スクリプト作成支援API仕様書 ✅
- [x] **👤 ユーザー確認**: API設計レビュー・承認 ✅
- [x] スクリプト作成者向けのヘルパー関数追加 ✅
- [x] JSON形式での構造情報出力機能 ✅
- [x] サンプルスクリプトとドキュメント作成 ✅
- [x] **👤 ユーザー確認**: API機能テスト・調整 ✅

**推定期間**: 2-3日（ユーザー確認時間含む）

### Phase 4: チュートリアル・ドキュメント強化 📚

#### 4.1 新機能チュートリアル作成
- [x] **設計書作成**: チュートリアル構成計画書 ✅
- [x] **👤 ユーザー確認**: チュートリアル構成レビュー・承認 ✅
- [x] Tutorial 9: 新しいテンプレート作成方法のチュートリアル（Scaffolding形式、entry-points登録） ✅
- [x] Tutorial 10: 情報提供APIを使ったscaffoldingツール作成ガイド（CLI、インタラクティブUI） ✅
- [x] Tutorial 11: パッケージ開発者向け実践的なサンプル作成（RAGシステム実例） ✅
- [ ] **👤 ユーザー確認**: チュートリアル内容レビュー・修正

#### 4.2 テスト・検証
- [x] **設計書作成**: 包括的テスト計画書 ✅
- [x] **👤 ユーザー確認**: テスト戦略レビュー・承認 ✅
- [x] 新機能の包括的テストスイート作成 ✅
- [x] 既存機能の回帰テスト実施 ✅
- [x] **👤 ユーザー確認**: テスト結果レビュー・問題対応 ✅
- [x] チュートリアルの動作確認・検証実施 ✅
- [x] **👤 ユーザー確認**: 検証結果最終確認・承認 ✅

**推定期間**: 2-3日（ユーザー確認時間含む）

### Phase 5: ドキュメント・エコシステム 📚

#### 5.1 ドキュメント作成
- [ ] **設計書作成**: ドキュメント構成計画書
- [ ] **👤 ユーザー確認**: ドキュメント構成レビュー・承認
- [ ] スキャフォールディング機能の使用方法ドキュメント作成
- [ ] 新テンプレート形式の移行ガイド作成
- [ ] APIリファレンス更新
- [ ] **👤 ユーザー確認**: ドキュメント内容レビュー・修正
- [ ] チュートリアルへの統合実装

#### 5.2 エコシステム対応
- [ ] **設計書作成**: エコシステム統合計画書
- [ ] **👤 ユーザー確認**: エコシステム計画レビュー・承認
- [ ] 既存チュートリアルの更新実施
- [ ] README.mdの機能説明追加
- [ ] プラグイン開発者向けガイド作成
- [ ] **👤 ユーザー確認**: ガイド・例示プロジェクト確認
- [ ] 例示プロジェクト作成
- [ ] **👤 ユーザー確認**: 全体ドキュメント最終レビュー・承認

**推定期間**: 2-3日（ユーザー確認時間含む）

## 技術実装詳細

### 簡素化されたデータモデル案

```python
# models.py 拡張
class EnvOption(BaseModel):
    category: str
    option: str
    env: Dict[str, EnvVarConfig]
    
# 削除されたモデル:
# - ScaffoldingTemplate (パッケージ側で管理)
# - ScaffoldingChoice (利用側で判断)
```

### 簡素化されたAPI実装案

```python
# core.py 拡張
def get_all_template_structure() -> Dict[str, List[str]]:
    """全テンプレート構造をカテゴリ別オプション一覧で返却"""
    
def has_category(category: str) -> bool:
    """指定カテゴリの存在確認"""
    
def get_options(category: str) -> List[str]:
    """カテゴリ内の全オプション取得"""
    
def generate_template(dest: str, generation_range: List[Dict[str, str]]) -> str:
    """選択的テンプレート生成（利用側が直接指定）"""
```

### CLI拡張案

```bash
# インタラクティブモード
oneenv scaffold --interactive

# 設定ファイル指定
oneenv scaffold --config scaffold.yaml

# 特定カテゴリのみ
oneenv scaffold --category vectorstore --category rag

# プレビューモード
oneenv scaffold --dry-run --config scaffold.yaml
```

## リスク分析・対策

### 技術リスク
- **複雑性増加**: 段階的実装で複雑性を管理
- **パフォーマンス**: キャッシュ機構とレイジーローディング
- **互換性**: 徹底した回帰テストと互換性レイヤー

### ユーザーエクスペリエンスリスク
- **学習コスト**: 既存機能は変更なし、新機能は追加のみ
- **設定複雑化**: デフォルト動作は現在と同じ、オプトイン方式

### エコシステムリスク
- **パッケージ対応**: 既存形式は継続サポート、移行は任意
- **ドキュメント**: 段階的ドキュメント更新計画

## 成功基準

### 機能面
- ✅ RAGスタック選択のデモが動作
- ✅ 既存機能への影響なし
- ✅ 新旧形式の完全互換性

### ユーザビリティ面
- ✅ 5分以内で基本的なスキャフォールディング完了
- ✅ 直感的なインタラクティブUI
- ✅ 明確なエラーメッセージとガイダンス

### エコシステム面
- ✅ プラグイン開発者向けドキュメント完備
- ✅ 移行ガイドライン提供
- ✅ コミュニティからの正のフィードバック

## 次のアクション

### 即座に着手
1. **Phase 1.1**: 新データモデル設計（`EnvOption`, `ScaffoldingTemplate`）
2. **基本API**: `get_all_template_structure()` のプロトタイプ実装
3. **テスト**: 新形式テンプレートの基本テスト作成

### 週内目標
- Phase 1の完了
- 基本的なスキャフォールディング機能のプロトタイプ
- 既存機能への影響評価

---

**重要**: この実装は既存OneEnvの価値を損なうことなく、新たな価値を追加することを最優先とする。