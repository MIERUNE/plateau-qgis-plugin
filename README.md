# plateau-qgis-plugin-rev2

[PoC]

QGIS 3.28 で動作させるため、Python 3.9 の文法で実装する必要があります。

## 実行

QGIS を使わずにテスト実行:

```console
cd plateau_plugin
python3 -m plateau /path/to/city/udx/luse/563846_luse_6668_op.gml
```

QGIS にデプロイ (macOS):

```console
make deploy
```
