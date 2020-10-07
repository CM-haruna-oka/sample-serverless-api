# Sample Serverless API
AWSのAPI Gateway + Lambdaを用いた基本的なサーバーレスAPIです。

エディタにVScode、Linterにpylint、スタイル規約にPEP8、コード整形にautopep8を使っています。

## 使用ツール
- バージョン管理: pyenv
- パッケージ管理+仮想環境: [Pipenv](https://pipenv-ja.readthedocs.io/ja/translate-ja/) (pip + virtualenv)
- Linter: pylint
- Formatter: autopep8
- Serverless Framework 
  - [serverless-python-requirements](https://www.serverless.com/plugins/serverless-python-requirements)
  - [serverless-offline](https://github.com/dherault/serverless-offline)

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

上記のコマンドでpipfileの中身がインストールされる。
（--devをつけると開発用パッケージもインストール）

パッケージを追加したい場合は以下のように実行する。

```
(例)
$ pipenv install numpy
```

バージョン指定

```
(例)
$ pipenv install numpy==1.14
```

開発用ライブラリ

```
(例)
$ pipenv install --dev autopep8
```

インストール済パッケージのアップデート
```
$ pipenv update
```

## serverless framework

```
$ npm install -g serverless

プラグインをインストール
$ npm install
```

## 設定ファイル
### 環境変数

環境毎に切り替えたい環境変数は `./config/config.${env}.yaml` に追記してください。

- `./config/config.itg.yaml`
- `./config/config.stg.yaml`
- `./config/config.prd.yaml`

configファイルに追加した変数をLambdaで参照するには、 `serverless.yaml` の `provider.environment`にも追加する必要があります。

例) 
```yaml
provider:
  environment:
    ENV: ${self:custom.environments.ENV}
```

### シークレット情報

シークレット情報はコミットに含めずにローカルのみに保存してください。
`./config/secret/` に `secret.${env}.yaml` を作成してください。


例) seccret.itg.yaml
```
USER_NAME: hoge
PASSWORD: hoge
```

### AWS CLIのプロファイル設定

~/.aws/credentials
```
[sls-itg]
aws_access_key_id = xxxx
aws_secret_access_key = xTXfcVxxxxxxxxxxxxxxxxxGlCb1CY2/l

[sls-stg]
aws_access_key_id=xxxx
aws_secret_access_key=wb6E12vExxxxxxxxxxxxxxxxxmNpUfWHZDB2

[sls-prd]
aws_access_key_id=xxxx
aws_secret_access_key=KJ+JISxxxxxxxxxxxxxxxxxwwJeZ86jEqG
```

## デプロイ

```
$ sls deploy 
デフォルトは開発アカウント（itg）にデプロイ

$ sls deploy --stage=stg
検証アカウントにデプロイ

$ sls deploy --stage=prd
本番環境にデプロイ
```


## lambdaの実行

```
$ sls invoke -f ListItems
$ sls invoke -f ListItems -p tests/event/list_items/event.json
```

###  ローカル実行

```
$ sls invoke local -f ListItems
```


