# -*- coding: utf-8 -*-

"""RDP"""

from albert import *;
import yaml;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "RDP";
__version__ = "0.0.1";
__triggers__ = "rdp ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("desktop");

rdpItems = [];

ALLOWED_COMMANDS = [
    "xfreerdp",
    "rdesktop",
    "remmina",
    "virt-viewer",
];

def make_rdp_item(title: str, command: str) -> Item:
    title = title.strip();
    command = command.strip();

    # check if command is allowed
    if list(filter(command.startswith, ALLOWED_COMMANDS)) == []:
        return None;

    return Item(
        id=f"rdp_{title}",
        icon=iconPath,
        text=title,
        subtext=command,
        completion=f"{command}", # autocomplete actual command
        urgency=ItemBase.Normal,
        actions=[
            ProcAction(text="Connect", commandline=["sh", "-c", command]),
            ClipAction(text="Copy command to clipboard", clipboardText=command),
        ],
    );

def initialize():
    global rdpItems;

    yaml_file = module_path + "/config.yml";
    if os.path.exists(yaml_file):
        info("Loading RDP config...");
        with open(yaml_file, "r") as stream:
            try:
                config = yaml.safe_load(stream);
                for command in config:
                    rdpItem = make_rdp_item(command["title"], command["command"]);
                    if rdpItem != None:
                        rdpItems.append(rdpItem);
            except yaml.YAMLError as e:
                critical(str(e));

def filtered_rdp_items(query: str) -> list[Item]:
    filtered = [];

    for rdpItem in rdpItems:
        if query in rdpItem.text.lower() or query in rdpItem.subtext.lower():
            filtered.append(rdpItem);

    return filtered;

def parse(query: str) -> str:
    return query.strip().lower();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    albertQuery.disableSort();

    # on empty query, return entire list
    if len(query) == 0:
        return rdpItems;

    return filtered_rdp_items(query);
