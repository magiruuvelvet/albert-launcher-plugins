# -*- coding: utf-8 -*-

"""Help"""

from albert import *;

try:
    import yaml;
    hasYaml = True;
except ImportError:
    hasYaml = False;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "help";
__version__ = "0.0.1";
__triggers__ = "help";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("help-hint");

helpItems = [];

def parse(query: str) -> str:
    return query.strip().lower();

def make_help_item(helpTitle: str, helpDescription: str) -> Item:
    return Item(
        id=f"help_{helpTitle}",
        icon=iconPath,
        text=helpTitle,
        subtext=helpDescription,
        completion=f"{helpTitle}", # autocomplete actual command
        urgency=ItemBase.Normal,
        actions=[],
    );

def initialize():
    global helpItems;
    global hasYaml;

    # built-in commands from my plugins
    helpItems = [
        make_help_item("dns",   "DNS Lookup"),
        make_help_item("http",  "Query HTTP Codes"),
        make_help_item("ip",    "Interface IP Lookup"),
        make_help_item("kiten", "Query Kiten Japanese Dictionary"),
        make_help_item("ps",    "Process Utilities"),
        make_help_item("pwd",   "Query D-Bus Secret Service API"),
        make_help_item("uuidgen", "Generate random UUID"),
        make_help_item("rdp",   "Connect to RDP"),
        make_help_item("virsh", "Virtual Machine Manager"),
    ];

    # additional user commands to show
    if hasYaml:
        yaml_file = module_path + "/commands.yml";
        if os.path.exists(yaml_file):
            info("Loading additional user commands...");
            with open(yaml_file, "r") as stream:
                try:
                    user_commands = yaml.safe_load(stream);
                    for command in user_commands["commands"]:
                        helpItems.append(make_help_item(command["title"], command["description"]));
                except yaml.YAMLError as e:
                    critical(str(e));

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    # return all help items on empty query
    if len(query) == 0:
        return helpItems;

    # ensure whitespace after trigger before doing filtering
    if len(query) > 0 and not albertQuery.string.startswith(" "):
        return [];

    # filter help items when filtering was requested
    filteredHelpItems = [];

    for item in helpItems:
        if query in item.text.lower() or query in item.subtext.lower():
            filteredHelpItems.append(item);

    return filteredHelpItems;
