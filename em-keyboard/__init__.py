# -*- coding: utf-8 -*-

"""Emoji Keyboard"""

from albert import *;

import os;
import em;

__title__ = "Emoji Keyboard";
__version__ = "0.0.1";
__triggers__ = "em ";
__authors__ = "マギルゥーベルベット";
__py_deps__ = "em";

# iconPath = iconLookup("");

emojis = None;

def initialize():
    # parse default emojis
    global emojis;
    emojis = em.parse_emojis();

    # parse user-defined emojis
    if os.path.isfile(em.CUSTOM_EMOJI_PATH):
        emojis.update(em.parse_emojis(em.CUSTOM_EMOJI_PATH));

def parse(query: str) -> str:
    return query.strip();

# lookup matching emojis
def find(query: str) -> tuple[str, str]:
    query = [query];
    names = tuple(map(em.clean_name, query));
    return em.do_find(emojis, names[0]);

def create_items(lookup: tuple[str, str]) -> list[Item]:
    items = [];

    for (name, emoji) in lookup:
        items.append(Item(
            id=f"emoji_{name}",
            text=emoji,
            subtext=name,
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="Copy emoji to clipboard", clipboardText=emoji),
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
    return create_items(find(query));
