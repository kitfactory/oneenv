# OneEnv 改善計画

## 背景・課題

現在のOneEnvライブラリは、外部パッケージから`@oneenv`デコレータを通じて環境変数テンプレートを取得し、`.env.example`ファイルに集約している。しかし、以下の課題がある：

1. **モジュール検出の不安定性**: `import_templates()`による自動検出は不確実
2. **型安全性の欠如**: 辞書形式での返値は実行時エラーのリスク
3. **拡張性の制限**: デコレータベースの仕組みは柔軟性に欠ける

## 改善提案

### 1. Entry-pointsベースのプラグインシステム
`pyproject.toml`の`[project.entry-points."oneenv.func"]`を使用して、外部パッケージが環境変数テンプレート関数を登録する仕組みに変更。

### 2. Pydanticモデルによる型安全性
環境変数スキーマをPydanticモデルで定義し、返値の型安全性と検証を強化。

## 実装計画

### Phase 1: 新システム設計・調査 🔍
- [ ] entry-pointsメカニズムの調査と設計
- [ ] pydanticモデル設計
- [ ] 既存システムとの互換性検討

### Phase 2: 実装 ⚙️
- [ ] pydanticモデルの実装
- [ ] entry-points検出システムの実装
- [ ] 既存デコレータシステムとの並行動作

### Phase 3: 移行・テスト 🧪
- [ ] 既存テストの更新
- [ ] 新システム向けテストの追加
- [ ] 移行ガイドの作成

### Phase 4: ドキュメント更新 📚
- [ ] README.mdの更新
- [ ] 使用例の更新
- [ ] CLAUDE.mdの更新

## 技術仕様案

### Entry-points設定例
```toml
[project.entry-points."oneenv.providers"]
my_package = "my_package.env:get_env_template"
```

### Pydanticモデル案
```python
from pydantic import BaseModel
from typing import List, Optional

class EnvVarSchema(BaseModel):
    description: str
    default: Optional[str] = ""
    required: bool = False
    choices: Optional[List[str]] = None

class EnvTemplate(BaseModel):
    variables: Dict[str, EnvVarSchema]
    source: str
```

## 移行戦略

### 段階的移行アプローチ
1. **Phase 1 - 新システム実装**: 既存システムと並行動作する新システムを実装
2. **Phase 2 - 互換性レイヤー**: 既存APIを新システムで提供
3. **Phase 3 - 段階的移行**: 既存機能を新システムに置き換え
4. **Phase 4 - レガシー廃止**: 十分なテスト後、レガシーシステムを削除

### 後方互換性の保証
- 既存の`@oneenv`デコレータは継続サポート
- 既存のAPIシグネチャは維持
- 辞書形式の返値も継続サポート
- 段階的な移行パスを提供

## 技術実装詳細

### 完了済み ✅
- **Pydanticモデル設計**: `models.py`で型安全な環境変数スキーマを定義
- **Entry-pointsコア実装**: `core.py`でプラグインシステムを実装
- **依存関係追加**: `pyproject.toml`にpydantic等を追加

### 実装されたファイル
- `src/oneenv/models.py` - Pydanticモデル定義
- `src/oneenv/core.py` - 新しいコアシステム
- `pyproject.toml` - 依存関係更新

## 実装完了状況

### ✅ 完了済み
- [x] TODO.md作成と計画策定
- [x] Entry-pointsシステム調査・設計  
- [x] Pydanticモデル設計・実装
- [x] 新コアシステム実装
- [x] 既存__init__.pyとの統合
- [x] CLIの更新（debugパラメータ対応）
- [x] 新システム向けテストの追加
- [x] 後方互換性の確保

### 🎯 主要成果

#### 1. Entry-pointsプラグインシステム
- `[project.entry-points."oneenv.templates"]`をサポート
- 外部パッケージから自動的にテンプレートを発見・読み込み
- プラグインとレガシーシステムの統合

#### 2. Pydanticモデルによる型安全性
- `EnvVarConfig`、`EnvTemplate`、`TemplateCollection`モデル
- 実行時検証とエラーハンドリング
- 型安全なテンプレート処理

#### 3. 段階的移行アーキテクチャ
- 既存の`@oneenv`デコレータは完全互換
- 新システムと並行動作
- レガシーAPIシグネチャ維持

### 📁 実装ファイル
- `src/oneenv/models.py` - Pydanticモデル定義
- `src/oneenv/core.py` - 新コアシステム
- `src/oneenv/__init__.py` - 統合レイヤー（既存API維持）
- `tests/test_enhanced_system.py` - 新システムテスト
- `pyproject.toml` - 依存関係更新

### 🔧 動作確認済み機能
- ✅ Pydanticモデルでの型検証
- ✅ Entry-pointsプラグイン発見システム
- ✅ レガシーデコレータとの統合
- ✅ CLIのdebugパラメータ対応
- ✅ 新システムでのテンプレート生成
- ✅ 後方互換性

---

**実装完了**: OneEnvは新しいentry-pointsとPydanticベースのアーキテクチャに成功的に移行しました！