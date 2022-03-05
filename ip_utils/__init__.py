# -*- coding: utf-8 -*-

"""IP Utils"""

from albert import *;
import netifaces as ni;

__title__ = "IP Utils";
__version__ = "0.0.1";
__triggers__ = ["ip", "ip "];
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("network-card");

def parse(query: str) -> str:
    return query.strip();

def query_interface_ip(iface_name: str) -> str:
    if not iface_name in ni.interfaces():
        return "No such interface";

    iface = ni.ifaddresses(iface_name);
    if ni.AF_INET in iface:
        return iface[ni.AF_INET][0]["addr"];
    else:
        return "DOWN";

def query_interface_ips(query: str) -> list[list[str]]:
    results = [];
    for iface in ni.interfaces():
        if iface.startswith(query):
            results.append([iface, query_interface_ip(iface)]);
    return results;

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    albertQuery.disableSort();

    albertItems = [];

    for i in query_interface_ips(query):
        name = i[0];
        ip = i[1];

        albertItems.append(Item(
            id=__title__,
            icon=iconPath,
            subtext=ip,
            text=name,
            completion=f"{__triggers__[0]} {name}",
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="ClipAction", clipboardText=ip)
            ]
        ));

    return albertItems;
