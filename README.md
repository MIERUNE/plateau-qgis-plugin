# plateau-qgis-plugin

A QGIS plugin for loading the PLATEAU 3D City Models. (PLATEAU 3D 都市モデルを読み込むための QGIS プラグイン)

## License

License: GPL v2

This plugin contains [plateau-py](https://github.com/MIERUNE/plateau-py), which is licensed under the MIT License.

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
