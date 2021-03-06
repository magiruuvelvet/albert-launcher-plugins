# -*- coding: utf-8 -*-

"""DNS Lookup"""

from albert import *;
from time import sleep;
import dns.resolver;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

__title__ = "DNS Lookup";
__version__ = "0.0.1";
__triggers__ = "dns ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("internet-services");

def parse(query: str) -> list[str]:
    query = query.split();
    if len(query) != 2:
        return [];
    return query[0:2];

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);

    # when command didn't matched, show usage
    if len(query) == 0:
        return [Item(
            id=__title__,
            icon=iconPath,
            text=__title__,
            subtext="<b>Usage:</b> TYPE domain",
            urgency=ItemBase.Notification,
        )];

    sleep(0.5);

    albertQuery.disableSort();

    domain = query[1];
    rtype = query[0].upper();

    subtext = "DNS: " + rtype + " " + domain;

    try:
        results = dns.resolver.resolve(domain, rtype);
        albertItems = [];

        for res in results:
            dns_rec_text = res.to_text();
            albertItems.append(Item(
                id=__title__,
                icon=iconPath,
                subtext=subtext,
                text=dns_rec_text,
                completion=dns_rec_text,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="Copy to clipboard", clipboardText=dns_rec_text),
                ]
            ));

        return albertItems;

    except dns.resolver.NoAnswer:
        dns_rec_text = "No such record";
        return [
            Item(
                id=__title__,
                icon=iconPath,
                subtext=subtext,
                text=dns_rec_text,
                completion=dns_rec_text,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="Copy to clipboard", clipboardText=dns_rec_text),
                ]
            )
        ];
    except dns.resolver.NXDOMAIN:
        dns_rec_text = "NXDOMAIN";
        return [
            Item(
                id=__title__,
                icon=iconPath,
                subtext=subtext,
                text=dns_rec_text,
                completion=dns_rec_text,
                urgency=ItemBase.Normal,
                actions=[
                    ClipAction(text="Copy to clipboard", clipboardText=dns_rec_text),
                ]
            )
        ];
    except dns.rdatatype.UnknownRdatatype:
        return [];
