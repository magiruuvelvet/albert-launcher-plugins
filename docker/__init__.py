# -*- coding: utf-8 -*-

"""docker"""

from albert import *;
from typing import Union;
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

filter_function = filter;

STATUS_RUNNING: str = "running";
STATUS_EXITED: str = "exited";

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

def docker_containers(filter: str, filterByStatus: Union[str, None] = None, clipActionIsDefault: bool = True) -> list[Item]:
    items = [];

    if filterByStatus != None and filterByStatus == STATUS_RUNNING:
        containers = docker.from_env().containers.list(all=False);
    elif filterByStatus != None and filterByStatus == STATUS_EXITED:
        containers = docker.from_env().containers.list(all=True);
        containers = list(filter_function(lambda container: container.status == STATUS_EXITED, containers));
    else:
        containers = docker.from_env().containers.list(all=True);

    def sortByRunning(status: str) -> int:
        if status == STATUS_RUNNING: return 0;
        else: return 1;
    containers.sort(key=lambda container: sortByRunning(container.status));

    def colorize(status: str) -> str:
        if status == STATUS_RUNNING: return f"<font color='green'>{status}</font>";
        elif status == STATUS_EXITED: return f"<font color='red'>{status}</font>";
        else: return status;
    def start_stop_action(container) -> Union[dict, None]:
        if container.status == STATUS_RUNNING: return  {"text": "Stop Container",  "action": getattr(container, "stop")};
        elif container.status == STATUS_EXITED: return {"text": "Start Container", "action": getattr(container, "start")};
        else: return None;

    for container in containers:
        image_name = container.attrs["Config"]["Image"];
        if filter in container.name or filter in image_name:
            action = start_stop_action(container);
            item = Item(
                id=__title__,
                icon=iconPath,
                text=container.name,
                subtext=f"<b>Image:</b> {image_name}, <b>Status:</b> {colorize(container.status)}",
                urgency=ItemBase.Normal,
                # actions=[
                #     ClipAction(text="Copy to clipboard", clipboardText=f"Name: {container.name}, Image: {image_name}, Status: {container.status}"),
                #     FuncAction(text=action["text"], callable=lambda action=action: action["action"]()),
                # ],
            );

            # NOTE: item.actions.reverse() won't work here for some reason
            if clipActionIsDefault:
                item.actions = [
                    ClipAction(text="Copy to clipboard", clipboardText=f"Name: {container.name}, Image: {image_name}, Status: {container.status}"),
                    FuncAction(text=action["text"], callable=lambda action=action: action["action"]()),
                ];
            else:
                item.actions = [
                    FuncAction(text=action["text"], callable=lambda action=action: action["action"]()),
                    ClipAction(text="Copy to clipboard", clipboardText=f"Name: {container.name}, Image: {image_name}, Status: {container.status}"),
                ];

            items.append(item);

    return items;

def initialize():
    global commands;

    for i in [
        {"title": "images",  "desc": "Docker Images"},
        {"title": "ps",      "desc": "Docker Containers"},
        {"title": "start",   "desc": "Start Container"},
        {"title": "stop",    "desc": "Stop Container"},
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
        return docker_containers(filter=query.query);

    elif query.command.command == "start":
       return docker_containers(filter=query.query, filterByStatus=STATUS_EXITED, clipActionIsDefault=False);

    elif query.command.command == "stop":
        return docker_containers(filter=query.query, filterByStatus=STATUS_RUNNING, clipActionIsDefault=False);

    return albertItems;
