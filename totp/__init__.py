# -*- coding: utf-8 -*-

"""OTP Generator"""

from pydoc import cli
from albert import *;
from distutils.dir_util import mkpath;

import os;
import sys;
import keyring;

path = os.path.realpath(os.path.dirname(__file__));
sys.path.append(path);

import out.lib.libotpgenpy as otpgen;

__title__ = "OTP Generator";
__version__ = "0.0.1";
__triggers__ = "otp ";
__authors__ = "マギルゥーベルベット";
__py_deps__ = "keyring";

iconPath = iconLookup("otpgen");

# fixed location where the gui application creates the database file
otpgenDatabase = f"{os.getenv('HOME')}/.config/マギルゥーベルベット/OTPGen/database";
otpgen.setTokenFile(otpgenDatabase);

cachePath = None;
otpgenDatabaseStatus = None;
otpgenTokens = None;

def write_icon(filename: int, data: bytes):
    with open(f"{cachePath}/{filename}", "wb") as f:
        f.write(data);
        f.flush();

def initialize():
    # ensure cache location for icons exist
    global cachePath;
    cachePath = f"{cacheLocation()}/otpgen-icons";
    mkpath(cachePath);

    # load tokens from database
    global otpgenDatabaseStatus;
    global otpgenTokens;
    # receive the password from the same location as the gui application
    otpgen.setPassword(keyring.get_password("OTPGen", "secret"));
    otpgenDatabaseStatus = otpgen.loadTokens();

    if otpgenDatabaseStatus == 0:
        otpgenTokens = otpgen.getTokens();
        for token in otpgenTokens:
            if len(token["icon"]) > 0:
                write_icon(token["index"], token["icon"]);

def parse(query: str) -> str:
    return query.strip();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    if otpgenDatabaseStatus != 0:
        return Item(
            id=__title__,
            icon=iconPath,
            text=f"Failed to open database: {otpgenDatabaseStatus}",
            urgency=ItemBase.Alert,
        );

    # parse query
    query = parse(albertQuery.string);

    albertQuery.disableSort();

    # find matching tokens
    res = [tkn for tkn in otpgenTokens if query.lower() in tkn["label"].lower()];
    if len(res) == 0:
        return [];

    albertItems = [];

    for tkn in res:
        albertItems.append(Item(
            id=__title__,
            icon=f"{cachePath}/{tkn['index']}",
            text=tkn["label"],
            subtext=__title__,
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="Copy token to clipboard", clipboardText=otpgen.generateToken(tkn["index"])),
            ],
        ));

    return albertItems;
