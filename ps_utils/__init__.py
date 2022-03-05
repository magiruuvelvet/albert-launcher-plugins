# -*- coding: utf-8 -*-

"""PS Utils"""

from albert import *;
import enum;
from typing import Union

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

ps = importfile(module_path + "/ps.py");

__title__ = "PS Utils";
__version__ = "0.0.1";
__triggers__ = "ps ";
__authors__ = "マギルゥーベルベット";

# IDEA: get cpu usage and use -1,-2,-3,-4 variants of this icon
iconPath = iconLookup("task-process-0");

class Command(enum.Enum):
    Find  = "find";
    Debug = "debug";

def parse(query: str) -> Union[dict, str]:
    query = query.strip();

    comm = find_command(query);
    if comm:
        return comm;
    else:
        return query;

def make_help_item(command: Command, info: str) -> Item:
    return Item(
        id=__title__, icon=iconPath,
        text=command.value, subtext=info,
        completion=f"{__triggers__}{command.value} ",
        urgency=ItemBase.Normal, actions=[]);

commands = [];

def initialize():
    global commands;
    commands = [
        dict(command=Command.Find,  item=make_help_item(Command.Find,  "Search for processes")),
        #dict(command=Command.Debug, item=make_help_item(Command.Debug, "Debug command")),
    ];

def find_command(query: str) -> dict:
    for comm in commands:
        if query.startswith(comm["command"].value):
            return dict(command=comm["command"], query=query[len(comm["command"].value):].strip());
    return None;

def find_matching_commands(query: str) -> list[Item]:
    results = [];
    for comm in commands:
        if comm["command"].value.startswith(query):
            results.append(comm["item"]);
    return results;

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    # return available commands
    if type(query) == str:
        return find_matching_commands(query);

    albertQuery.disableSort();

    albertItems = [];

    if query["command"] == Command.Find:
        for proc in ps.filter_by_query(query["query"]):
            text = f"{proc['pid']} {proc['command']}";
            albertItems.append(Item(
                id=__title__,
                icon=iconPath,
                subtext=proc["cmdline"],
                text=text,
                completion=__triggers__,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="ClipAction", clipboardText=f"{text}\n{proc['cmdline']}\n"),
                ]
            ));

    return albertItems;
