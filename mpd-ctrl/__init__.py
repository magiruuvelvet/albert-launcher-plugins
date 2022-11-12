# -*- coding: utf-8 -*-

"""mpd controller"""

from albert import *;
from typing import Callable;
import yaml;
import os;
from mpd import MPDClient;
from time import sleep;

__title__ = "mpd controller";
__version__ = "0.0.1";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("mpd");

client: MPDClient = None;
socketFile = None;
configdir = os.path.join(configLocation(), "mpd");

def parse(query: str) -> str:
    return query.strip().lower();

def initialize():
    global client;

    info("Loading configuration...");
    global socketFile;

    if not os.path.exists(configdir):
        os.mkdir(configdir);
    configfile = configdir + "/config.yml";
    if os.path.exists(configfile):
        with open(configfile, "r") as stream:
            try:
                config = yaml.safe_load(stream);
                socketFile = config["socketFile"];
            except yaml.YAMLError as e:
                critical(str(e));

    # initialize client when socket file was specified in config
    if socketFile != None:
        client = MPDClient();

def call(function: Callable[[], Item]) -> Item:
    res = None;
    try:
        client.connect(socketFile);
        res = function();
    finally:
        client.disconnect();
    return res;

def currentsong() -> Item:
    song: dict[str, str] = client.currentsong();

    info = f"{song['artist']} ・ {song['title']} ・ {song['album']} ({song['date']})";

    return Item(
        id="00000-mpd-currentsong",
        icon=iconPath,
        text=song["title"],
        subtext=f"<b>{song['artist']}</b> ・ {song['album']} ({song['date']})",
        completion=info,
        urgency=ItemBase.Alert,
        actions=[
            ClipAction(text="Copy song info to clipboard", clipboardText=info),
        ],
    );

def handleQuery(albertQuery: Query) -> list[Item]:
    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0 or not query.startswith("."):
        return [];

    albertQuery.disableSort();

    if query == ".song" or query == ".currentsong":
        return call(currentsong);
    else:
        return [];
