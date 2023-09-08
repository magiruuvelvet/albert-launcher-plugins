# -*- coding: utf-8 -*-

"""edit"""

from albert import *;
from typing import Union;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "edit";
__version__ = "0.0.1";
__triggers__ = "edit ";
__authors__ = "マギルゥーベルベット";

# TODO: customize icon with config file
iconPath = iconLookup("kwrite");

# TODO: editor list with config file + file extensions
def determine_editor(path: str) -> str:
    #if path.endswith(".txt")
    return "kwrite";

def resolve_path(path: str) -> Union[dict, None]:
    # strip left whitespaces
    path = path.lstrip();

    if len(path) == 0:
        return None;

    # resolve tilde
    if path == "~":
        return None;
    if path.startswith("~/"):
        path = os.path.join(os.getenv("HOME"), path[2:]);

    # check if directory
    if os.path.isdir(path):
        return None;

    # check if existing file
    if os.path.isfile(path):
        return {"path": path, "exists": True};

    # file doesn't exist yet
    return {"path": path, "exists": False};

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # resolve given path to get a file path
    file = resolve_path(albertQuery.string);
    if file == None:
        return [];

    albertQuery.disableSort();

    editor = determine_editor(file);

    # TODO: notify that no editor is capable to edit this file
    if len(editor) == 0:
        return [];

    if file['exists']:
        itemText = f"Edit {albertQuery.string} in {editor}";
    else:
        itemText = f"Create {albertQuery.string} with {editor}";

    return Item(
        id=__title__,
        icon=iconPath,
        text=itemText,
        subtext=f"{editor} {file['path']}",
        urgency=ItemBase.Notification,
        actions=[
            ProcAction(text="Execute", commandline=[editor, file['path']]),
        ],
    )
