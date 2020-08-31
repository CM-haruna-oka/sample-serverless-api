# Sample Serverless API
AWSのAPI Gateway + Lambda + DynamoDBを用いた基本的なサーバーレスAPIです。

エディタにVScode、Linterにpylint、スタイル規約にPEP8、コード整形にautopep8を使っています。

## 使用ツール
- バージョン管理: pyenv
- パッケージ管理+仮想環境: [Pipenv](https://pipenv-ja.readthedocs.io/ja/translate-ja/) (pip + virtualenv)
- Linter: pylint
- Formatter: autopep8
- Serverless Framework

## コーディング規約

[PEP8](https://pep8-ja.readthedocs.io/ja/latest/): Python標準ライブラリに含まれるコーディング規約

## 仮想環境の作成

- pipenvが入っていない場合はインストール

```bash
$ brew install pipenv
```

### pipenvの使い方

PIPENV_VENV_IN_PROJECTをtrueにしてプロジェクトディレクトリに仮想環境を作成する。

```bash
$ export PIPENV_VENV_IN_PROJECT=true
$ pipenv shell
```

仮想環境を抜ける
```
$ exit
```

## 依存ライブラリのインストール
仮想環境に入ったら、依存ライブラリをインストールする。

```bash
$ pipenv install --dev
```

--devをつけると開発用パッケージもインストールされます。

## デプロイ

```
$ sls deploy
```

## lambdaの実行

```
$ sls invoke -f listPromotionalItems
```

ローカル実行

```
$ sls invoke local -f listPromotionalItems
```

### VScode Settings

```
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.lintOnSave": true,
  "python.formatting.provider": "autopep8",
  "editor.formatOnSave": true,
  "python.pythonPath": ".venv/bin/python"
}
```

- python.linting.enabled ••• Lint有効化
- python.linting.pylintEnabled ••• pylint有効化
- python.linting.lintOnSave ••• ファイル保存時にLint実行
- python.formatting.provider ••• フォーマッターに何を使用するか
- editor.formatOnSave ••• ファイル保存時にフォーマット実行
- python.pythonPath ••• 使用するpythonコマンドへのパス

