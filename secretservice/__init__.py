# -*- coding: utf-8 -*-

"""Secret Service"""

from albert import *;
import secretstorage;
from contextlib import closing;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

secretservice = importfile(module_path + "/secretservice.py");

__title__ = "Secret Service";
__version__ = "0.0.1";
__triggers__ = "pwd ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("password-copy");
iconError = iconLookup("dialog-error");

def parse(query: str) -> str:
    return query.strip();

def make_error_item(message: str) -> Item:
    return Item(
        id=__title__,
        icon=iconError,
        text=message,
        subtext="Secret Service",
        urgency=ItemBase.Alert,
        actions=[],
    );

def make_secret_items(collection: secretstorage.Collection, query: str) -> list[Item]:
    items = [];

    for match in secretservice.query(collection, query):
        items.append(Item(
            id=__title__,
            icon=iconPath,
            text=match["label"],
            subtext="Secret Service",
            urgency=ItemBase.Normal,
            actions=[
                FuncAction(text="Copy to clipboard", callable=lambda item_path=match["item_path"]: secretservice.copy(item_path)),
            ],
        ));

    return items;

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    albertQuery.disableSort();

    try:
        with closing(secretstorage.dbus_init()) as dbus:
            collection = secretstorage.get_default_collection(dbus);
            return make_secret_items(collection, query);
    except Exception as e:
        return [make_error_item(str(e))];
