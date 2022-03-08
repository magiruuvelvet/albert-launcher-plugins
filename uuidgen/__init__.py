# -*- coding: utf-8 -*-

"""UUID Generator"""

from albert import *;
import uuid;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

# dep = importfile(module_path + "/dep.py");

__title__ = "UUID Generator";
__version__ = "0.0.1";
__triggers__ = "uuidgen";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("dialog-password");

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    generated_uuid = str(uuid.uuid4());

    return [
        Item(
            id=__title__,
            icon=iconPath,
            text=generated_uuid,
            completion=generated_uuid,
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="Copy to clipboard", clipboardText=generated_uuid),
            ],
        )
    ];
