# -*- coding: utf-8 -*-

"""virt-manager"""

# Plugin very much work in progress
# only lists available VMs for now

from albert import *;
from contextlib import closing;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

virtmanager = importfile(module_path + "/virtmanager.py");

__title__ = "virt-manager";
__version__ = "0.0.1";
__triggers__ = "virsh ";
__authors__ = "マギルゥーベルベット";

iconMain     = iconLookup("virt-manager");
iconRunning  = iconLookup("media-playback-playing");
iconStopped  = iconLookup("media-playback-stopped");
iconBoot     = iconLookup("media-playback-start");
iconShutdown = iconLookup("media-playback-stop");

def determineVMIcon(status: bool) -> str:
    if status:
        return iconRunning;
    else:
        return iconStopped;

def activeText(status: bool) -> str:
    if status:
        return "Running";
    else:
        return "Stopped";

def domainSubtext(domain) -> str:
    return f"{activeText(domain['active'])}";

def listVMs(filter: str = None) -> list[Item]:
    items = [];
    with closing(virtmanager.VirtManager()) as virt:
        for domain in virt.getDomainsSorted():
            if filter != None:
                if not filter in domain["name"]:
                    continue;

            items.append(Item(
                id=f"libvirt_{domain['uuid']}",
                icon=determineVMIcon(domain["active"]),
                text=domain["name"],
                subtext=domainSubtext(domain),
                #completion="",
                urgency=ItemBase.Normal,
                actions=[],
            ));
    return items;

def parse(query: str) -> str:
    return query.strip().lower();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    albertQuery.disableSort();

    # list all VMs on empty query
    if len(query) == 0:
        return listVMs();

    # list VMs filtered
    return listVMs(query);
