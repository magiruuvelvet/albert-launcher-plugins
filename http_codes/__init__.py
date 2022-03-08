# -*- coding: utf-8 -*-

"""HTTP Status Codes"""

from albert import *;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

http = importfile(module_path + "/http.py");

__title__ = "HTTP Status Codes";
__version__ = "0.0.1";
__triggers__ = "http ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("internet-services");

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

    for i in http.find_match(query):
        albertItems.append(Item(
            id=__title__,
            icon=iconPath,
            subtext=i[1],
            text=i[0],
            completion=__triggers__,
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="Copy to clipboard", clipboardText=i[0] + " " + i[1]),
                UrlAction(text="Open in httpstatuses.com", url="https://httpstatuses.com/" + i[0]),
            ]
        ));

    return albertItems;
