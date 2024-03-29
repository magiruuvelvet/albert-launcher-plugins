# -*- coding: utf-8 -*-

"""mpv"""

from albert import *;
import yaml;
import socket;
from random import randrange;
from distutils.dir_util import mkpath;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

indexer = importfile(module_path + "/indexer.py");

__title__ = "mpv";
__version__ = "0.0.1";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("mpv");
cachePath = None;

mpv_bin = "mpv";
mpv_args = ["--player-operation-mode=pseudo-gui", "--profile=albert-launcher"];

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

    # ensure cache location for thumbnails exist
    global cachePath;
    cachePath = f"{cacheLocation()}/mpvthumbnails";
    mkpath(cachePath);

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
        mpv_fileList = indexer.get_all_files(rootDir, cachePath);
        info(f"Found {len(mpv_fileList)} media files.");

def send_command(command: str):
    if socketFile == None or len(socketFile) == 0:
        warning("mpv socket file not specified, append feature not available.");
        return;

    try:
        mpv_socket = socket.socket(socket.AF_UNIX);
        mpv_socket.connect(socketFile);
        mpv_socket.send(command.encode("utf-8"));
    except ConnectionError:
        pass;
    finally:
        mpv_socket.close();

def append(file: str) -> None:
    # escape path for "loadfile" command
    file = file.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
    file = "\"" + file + "\"";

    send_command("raw loadfile " + file + " append\n");

def play():
    command = '{ "command": ["set_property", "pause", false] }';
    send_command(f"{command}\n");
def pause():
    command = '{ "command": ["set_property", "pause", true] }';
    send_command(f"{command}\n");

def make_mpv_item(file: str) -> Item:
    return Item(
        id=__title__,
        icon=file["iconPath"] if file["iconPath"] != None else iconPath,
        subtext=file["nameFull"],
        text=file["nameBase"],
        completion=file["nameFull"],
        urgency=ItemBase.Normal,
        actions=[
            ProcAction(text="再生", commandline=[mpv_bin, *mpv_args, file["path"]]),
            FuncAction(text="プレイリストに追加", callable=lambda file=file["path"]: append(file)),
            ProcAction(text="ループ再生", commandline=[mpv_bin, *mpv_args, "--loop", file["path"]]),
            ProcAction(text="ディレクトリを開く", commandline=["xdg-open", file["dir"]]),
        ]
    );

def make_playback_item(title: str, function: callable) -> Item:
    return Item(
        id=__title__,
        icon=iconPath,
        text=title,
        urgency=ItemBase.Notification,
        actions=[
            FuncAction(text=title, callable=function),
        ],
    );

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

    # random item requested
    if query.startswith("mpv random"):
        random_index = randrange(len(mpv_fileList))
        return make_mpv_item(mpv_fileList[random_index]);
    # play requested
    if query == "mpv play":
        return make_playback_item("Play", play);
    # pause requested
    if query == "mpv pause":
        return make_playback_item("Pause", pause);

    albertItems = [];

    # split query at whitespaces
    query = query.split();
    if (len(query) == 0):
        return [];

    for file in mpv_fileList:
        #if query in file["nameFullLower"]:
        if all(x in file["nameFullLower"] for x in query):
            albertItems.append(make_mpv_item(file));

    return albertItems;
