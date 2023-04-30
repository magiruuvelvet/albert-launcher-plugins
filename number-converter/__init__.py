# -*- coding: utf-8 -*-

""""""

from albert import *;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

kanji = importfile(module_path + "/kanji.py");

__title__ = "Number Converter";
__version__ = "0.0.1";
__authors__ = "マギルゥーベルベット";

# iconPath = iconLookup("");

def parse(query: str) -> str:
    return query.strip();

def handleQuery(albertQuery: Query) -> list[Item]:
    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    albertQuery.disableSort();

    if normalized := kanji.kanji2dec(query):
        return [Item(
            id=__title__,
            text=f"{normalized}",
            subtext=query,
            completion=f"{normalized}")];

    return [];
