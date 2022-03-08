# -*- coding: utf-8 -*-

"""mpv"""

from albert import *;
import yaml;
import socket;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

indexer = importfile(module_path + "/indexer.py");

__title__ = "mpv";
__version__ = "0.0.1";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("mpv");

configdir = os.path.join(configLocation(), "mpv");

mpv_fileList = [];
socketFile = None;

def parse(query: str) -> str:
    return query.strip().lower();

def initialize():
    global mpv_fileList;

    info("Loading configuration...");
    rootDir = None;
    global socketFile;

    if not os.path.exists(configdir):
        os.mkdir(configdir);
    configfile = configdir + "/config.yml";
    if os.path.exists(configfile):
        with open(configfile, "r") as stream:
            try:
                config = yaml.safe_load(stream);
                rootDir = config["rootDir"];
                socketFile = config["socketFile"];
            except yaml.YAMLError as e:
                critical(str(e));

    if rootDir != None and len(rootDir) > 1:
        info(f"Scanning media files in {rootDir}...");
        mpv_fileList = indexer.get_all_files(rootDir);
        info(f"Found {len(mpv_fileList)} media files.");

def append(file: str) -> None:
    if socketFile == None or len(socketFile) == 0:
        warning("mpv socket file not specified, append feature not available.");
        return;

    # escape path for "loadfile" command
    file = file.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
    file = "\"" + file + "\"";

    try:
        mpv_socket = socket.socket(socket.AF_UNIX);
        mpv_socket.connect(socketFile);
        mpv_socket.send(("raw loadfile " + file + " append\n").encode("utf-8"));
    except ConnectionError:
        pass;
    finally:
        mpv_socket.close();

def handleQuery(albertQuery: Query) -> list[Item]:
    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    # don't search for these characters
    if query == "." or query == "/":
        return [];

    albertQuery.disableSort();

    if len(mpv_fileList) == 0:
        return [];

    albertItems = [];

    for file in mpv_fileList:
        if query in file["nameFullLower"]:
            albertItems.append(Item(
                id=__title__,
                icon=iconPath,
                subtext=file["nameFull"],
                text=file["nameBase"],
                completion=file["nameFull"],
                urgency=ItemBase.Normal,
                actions=[
                    ProcAction(text="再生", commandline=["mpv", file["path"]]),
                    FuncAction(text="プレイリストに追加", callable=lambda file=file["path"]: append(file)),
                ]
            ));

    return albertItems;
