Hanihoh Diagnosis
====

http://crittoo96.hatenablog.jp/entry/2019/10/08/143733

## Description
ハニホーの診断結果をTwitterから取得するスクリプト

## Demo
diagnosis.sqlにテーブル情報が入っているので、mysqlにログインしたあとに
```
source diagnosis.sql
```
でテーブルを作成。

```
touch ./config.py
```
でconfig.pyにCK, CS, AT, ATS変数を書き込み。APIを設定する。

main.pyでconfig.pyを読み込んで
```
$python main.py
```
で取得できる。 

## Requirement
1. python3
1. mysql

## Licence

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)

## Author

[crittoo96](https://github.com/crittoo96)
