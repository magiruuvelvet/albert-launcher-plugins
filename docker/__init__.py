# -*- coding: utf-8 -*-

"""docker"""

from albert import *;
from time import sleep;
import docker;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

commandlib = importfile(module_path + "/../lib/commandlib.py");

__title__ = "docker";
__version__ = "0.0.1";
__triggers__ = "docker ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup(module_path + "/docker.png");

commands = commandlib.CommandRegistry();

def docker_images(filter: str) -> list[Item]:
    items = [];

    images = docker.from_env().images.list();
    for image in images:
        for tag in image.tags:
            if filter in tag:
                items.append(Item(
                    id=__title__,
                    icon=iconPath,
                    text=tag,
                    subtext=image.id,
                    urgency=ItemBase.Normal,
                    actions=[
                        ClipAction(text="Copy to clipboard", clipboardText=f"{tag} {image.id}"),
                    ],
                ));

    return items;

def docker_containers(filter: str) -> list[Item]:
    items = [];

    containers = docker.from_env().containers.list(all=True);

    def sortByRunning(status: str) -> int:
        if status == "running": return 0;
        else: return 1;
    containers.sort(key=lambda container: sortByRunning(container.status));

    def colorize(status: str) -> str:
        if status == "running": return f"<font color='green'>{status}</font>";
        elif status == "exited": return f"<font color='red'>{status}</font>";
        else: return status;

    for container in containers:
        image_name = container.attrs["Config"]["Image"];
        if filter in container.name or filter in image_name:
            items.append(Item(
                id=__title__,
                icon=iconPath,
                text=container.name,
                subtext=f"<b>Image:</b> {image_name}, <b>Status:</b> {colorize(container.status)}",
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="Copy to clipboard", clipboardText=f"Name: {container.name}, Image: {image_name}, Status: {container.status}"),
                ],
            ));

    return items;

def initialize():
    global commands;

    for i in [
        {"title": "images",  "desc": "Docker Images"},
        {"title": "ps",      "desc": "Docker Containers"},
    ]:
        commands.addCommand(commandlib.Command(
            command=i["title"], description=i["desc"],
            completionPrefix=__triggers__, iconPath=iconPath, id=__title__), False);

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = commands.parse(albertQuery.string);

    # return available commands
    if type(query) == str:
        return commands.findMatchingCommands(query);

    albertQuery.disableSort();

    albertItems = [];

    # wait a little bit
    sleep(0.2);

    if query.command.command == "images":
        return docker_images(query.query);

    elif query.command.command == "ps":
        return docker_containers(query.query);

    return albertItems;
