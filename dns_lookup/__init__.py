# -*- coding: utf-8 -*-

"""DNS Lookup"""

from albert import *;
import dns.resolver;

__title__ = "DNS Lookup";
__version__ = "0.0.1";
__triggers__ = "dns ";
__authors__ = "マギルゥーベルベット";

def parse(query: str) -> list[str]:
    query = query.split(maxsplit=1);
    if len(query) != 2:
        return [];
    return query[0:2];

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    info("DNS: " + query[0] + " " + query[1]);

    try:
        results = dns.resolver.resolve(query[1], query[0]);
        albertItems = [];

        for res in results:
            item = Item(
                id=__title__,
                #icon=iconPath,
                subtext="DNS: " + query[0] + " " + query[1],
                text=res.to_text(),
                completion=__triggers__,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="ClipAction", clipboardText=res.to_text())
                ]
            );
            albertItems.append(item);

        return albertItems;

    except dns.resolver.NoAnswer:
        return [
            Item(
                id=__title__,
                #icon=iconPath,
                subtext="DNS: " + query[0] + " " + query[1],
                text="No such record",
                completion=__triggers__,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="ClipAction", clipboardText="No such record")
                ]
            )
        ];
    except dns.resolver.NXDOMAIN:
        return [
            Item(
                id=__title__,
                #icon=iconPath,
                subtext="DNS: " + query[0] + " " + query[1],
                text="NXDOMAIN",
                completion=__triggers__,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="ClipAction", clipboardText="NXDOMAIN")
                ]
            )
        ];
    except dns.rdatatype.UnknownRdatatype:
        return [];
