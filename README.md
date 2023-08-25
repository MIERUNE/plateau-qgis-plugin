# plateau-qgis-plugin

A QGIS plugin for loading PLATEAU 3D city models. (PLATEAU 3D 都市モデルを読み込むための QGIS プラグイン)

## 開発

- QGIS 3.28 で動作させるため Python 3.9 の文法で実装する必要があります。
- PLATEAU データのパーサなどは [plateau-py](https://github.com/MIERUNE/plateau-py) パッケージとして分離されています。

QGIS にデプロイする:

```console
make deploy
```

最新の `plateau-py` を取り込む:

```console
make update_dependencies
```
