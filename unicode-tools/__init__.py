# -*- coding: utf-8 -*-

"""Unicode Tools"""

from albert import *;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

uc = importfile(module_path + "/lib.py");

__title__ = "Unicode Tools";
__version__ = "0.0.1";
#__triggers__ = "";
__authors__ = "マギルゥーベルベット";

# icon may not be distributable, logo pulled from https://home.unicode.org
iconPath = module_path + "/unicode-logo.jpg";

def make_item(codepoint_info: dict[str, str]) -> Item:
    text = codepoint_info["name"];
    if "cp" in codepoint_info:
        text += f" ({codepoint_info['cp']})";

    return Item(
        id=__title__,
        icon=iconPath,
        text=text,
        subtext=codepoint_info["char"],
        urgency=ItemBase.Normal,
        completion=codepoint_info["char"],
        actions=[
            ClipAction(text="Copy character to clipboard", clipboardText=codepoint_info["char"]),
            ClipAction(text="Copy character name to clipboard", clipboardText=text),
        ],
    );

def parse(query: str) -> str:
    return query.strip();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    #if not albertQuery.isTriggered:
    #    return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    albertQuery.disableSort();

    # query needs to start with U+ for a single character lookup by codepoint
    if (query.startswith("U+") or query.startswith("u+")) and uc.uc_valid_query(query):
        if (codepoint_info := uc.uc_get_name(query[2:])) is not None:
            return make_item(codepoint_info);

    # search characters matching the given name
    elif query.startswith("unicode "):
        items = [];
        for codepoint_info in uc.uc_find_by_name(query[8:]):
            items.append(make_item(codepoint_info));
        return items;

    return [];
