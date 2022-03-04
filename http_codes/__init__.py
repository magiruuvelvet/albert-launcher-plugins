# -*- coding: utf-8 -*-

"""HTTP Status Codes"""

from albert import *;
import dns.resolver;

__title__ = "HTTP Status Codes";
__version__ = "0.0.1";
__triggers__ = "http ";
__authors__ = "マギルゥーベルベット";

iconPath = iconLookup("internet-services");

HTTP_STATUS_CODES = [
    ["100","Continue"],
    ["101","Switching protocols"],
    ["102","Processing"],
    ["103","Early Hints"],
    ["200","OK"],
    ["201","Created"],
    ["202","Accepted"],
    ["203","Non-Authoritative Information"],
    ["204","No Content"],
    ["205","Reset Content"],
    ["206","Partial Content"],
    ["207","Multi-Status"],
    ["208","Already Reported"],
    ["226","IM Used"],
    ["300","Multiple Choices"],
    ["301","Moved Permanently"],
    ["302","Found"],
    ["303","See Other"],
    ["304","Not Modified"],
    ["305","Use Proxy"],
    ["306","Switch Proxy"],
    ["307","Temporary Redirect"],
    ["308","Permanent Redirect"],
    ["400","Bad Request"],
    ["401","Unauthorized"],
    ["402","Payment Required"],
    ["403","Forbidden"],
    ["404","Not Found"],
    ["405","Method Not Allowed"],
    ["406","Not Acceptable"],
    ["407","Proxy Authentication Required"],
    ["408","Request Timeout"],
    ["409","Conflict"],
    ["410","Gone"],
    ["411","Length Required"],
    ["412","Precondition Failed"],
    ["413","Payload Too Large"],
    ["414","URI Too Long"],
    ["415","Unsupported Media Type"],
    ["416","Range Not Satisfiable"],
    ["417","Expectation Failed"],
    ["418","I'm a Teapot"],
    ["421","Misdirected Request"],
    ["422","Unprocessable Entity"],
    ["423","Locked"],
    ["424","Failed Dependency"],
    ["425","Too Early"],
    ["426","Upgrade Required"],
    ["428","Precondition Required"],
    ["429","Too Many Requests"],
    ["431","Request Header Fields Too Large"],
    ["451","Unavailable For Legal Reasons"],
    ["500","Internal Server Error"],
    ["501","Not Implemented"],
    ["502","Bad Gateway"],
    ["503","Service Unavailable"],
    ["504","Gateway Timeout"],
    ["505","HTTP Version Not Supported"],
    ["506","Variant Also Negotiates"],
    ["507","Insufficient Storage"],
    ["508","Loop Detected"],
    ["510","Not Extended"],
    ["511","Network Authentication Required"],
];

def find_match(query: str) -> list[list[str]]:
    results = [];
    for pair in HTTP_STATUS_CODES:
        if pair[0].startswith(query) or query.lower() in pair[1].lower():
            results.append(pair);
    return results;

def parse(query: str) -> str:
    return query.strip();

def handleQuery(albertQuery: Query) -> list[Item]:
    # check if the query has a trigger
    if not albertQuery.isTriggered:
        return [];

    # parse query
    query = parse(albertQuery.string);
    if len(query) == 0:
        return [];

    albertQuery.disableSort();

    albertItems = [];

    for i in find_match(query):
        item = Item(
            id=__title__,
            icon=iconPath,
            subtext=i[1],
            text=i[0],
            completion=__triggers__,
            urgency=ItemBase.Normal,
            actions=[
                ClipAction(text="ClipAction", clipboardText=i[0] + " " +i[1])
            ]
        );
        albertItems.append(item);

    return albertItems;
