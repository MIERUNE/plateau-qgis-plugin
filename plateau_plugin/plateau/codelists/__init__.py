"""コード表を扱う

事前定義されたコード表および配布物に含まれる自治体独自のコード表を扱う。
"""

from __future__ import annotations

import json
from pathlib import Path

import lxml.etree as et

from ..namespaces import BASE_NS as _NS


class CodelistStore:
    """事前定義されたコードリストまたは頒布データの ./codelists/ ディレクトリからコードを検索する"""

    def __init__(self, base_path: Path) -> None:
        self._base_path = base_path
        self._cached: dict[str, dict[str, str] | None] = {}
        self._predefined: dict[str, dict[str, str]] = {}

    def lookup(self, predefined_name: str | None, path: str | None, code: str) -> str:
        """事前定義されたコードリストまたは ./codelists/ ディレクトリ内のコードリストからコードを検索する"""

        # キャッシュされたコードリストがあればそこから取得する
        if path in self._cached:
            if (cache := self._cached[path]) is not None:
                return cache.get(code, code)
            return code

        # 事前定義されたコードリストから取得を試みる
        predefined = {}
        if predefined_name and (v := self.get_predefined(predefined_name).get(code)):
            return v

        if not path:
            return code

        # コードリストファイルからの取得を試みる
        # 取得結果はキャッシュすること
        cached = self._load_dictionary(predefined, path)
        return cached.get(code, code)

    def _load_dictionary(self, predefined: dict[str, str], path: str) -> dict[str, str]:
        """コードリスト (XML) を読み込む"""
        try:
            path_to_codes = (self._base_path / path).resolve()
            doc = et.parse(str(path_to_codes), None)
        except OSError:
            self._cached[str(path)] = predefined
            return predefined
        else:
            dictionary = {
                **predefined,
            }
            for entry in doc.iterfind(".//gml:dictionaryEntry", _NS):
                for definition in entry.iterfind(".//gml:Definition", _NS):
                    name = definition.find("./gml:name", _NS).text or ""
                    desc = definition.find("./gml:description", _NS).text or ""
                    dictionary[name] = desc.replace("\u3000", " ").strip()
            self._cached[str(path)] = dictionary
            return dictionary

    def get_predefined(self, name: str) -> dict[str, str]:
        """事前定義されたコードリスト一覧からコードリストを取得する"""
        if not self._predefined:
            with open((Path(__file__).parent / "codelists.json").resolve()) as f:
                self._predefined = json.load(f)

        return self._predefined[name]
