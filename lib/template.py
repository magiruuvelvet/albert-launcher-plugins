# -*- coding: utf-8 -*-

""""""

from albert import *;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "";
__version__ = "0.0.1";
__triggers__ = "";
__authors__ = "マギルゥーベルベット";

# iconPath = iconLookup("");

def parse(query: str) -> str:
    return query.strip();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    albertQuery.disableSort();

    albertItems = [];

    return albertItems;
