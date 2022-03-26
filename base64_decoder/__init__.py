# -*- coding: utf-8 -*-

"""base64 decoder"""

import base64
from albert import *;
from typing import Union;
from enum import Enum;

import base64;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "base64 decoder";
__version__ = "0.0.1";
__triggers__ = ["base32 ", "base64 "];
__authors__ = "マギルゥーベルベット";

# iconPath = iconLookup("");

class Mode(Enum):
    Base32 = 0x32;
    Base64 = 0x64;

def parse(query: str) -> str:
    return query.strip();

def parseMode(query: str) -> Union[Mode, None]:
    if query.startswith("base32 "):
        return Mode.Base32;
    elif query.startswith("base64 "):
        return Mode.Base64;
    return None;

# decode base64 without throwing exception, return None instead
def base64_decode(encoded: str) -> Union[str, None]:
    try:
        return base64.b64decode(encoded).decode("utf-8", "ignore");
    except:
        return None;

# decode base32 without throwing exception, return None instead
def base32_decode(encoded: str) -> Union[str, None]:
    try:
        return base64.b32decode(encoded).decode("utf-8", "ignore");
    except:
        return None;

def make_item(text: str, subtext: str, clipboardText: str) -> Item:
    return Item(
        id=__title__,
        icon="",
        text=text,
        subtext=subtext,
        urgency=ItemBase.Normal,
        actions=[
            ClipAction(text="Copy results to clipboard", clipboardText=clipboardText),
        ],
    );

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    # determine mode
    mode = parseMode(albertQuery.rawString);

    albertQuery.disableSort();

    if mode == Mode.Base32:
        decoded = base32_decode(query);
        if decoded != None:
            return make_item(decoded, "base32", decoded);

    elif mode == Mode.Base64:
        decoded = base64_decode(query);
        if decoded != None:
            return make_item(decoded, "base64", decoded);

    return [];
