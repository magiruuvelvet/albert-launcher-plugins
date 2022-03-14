# -*- coding: utf-8 -*-

"""PS Utils"""

from albert import *;
import signal;

import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

ps = importfile(module_path + "/ps.py");
commandlib = importfile(module_path + "/../lib/commandlib.py");

__title__ = "PS Utils";
__version__ = "0.0.1";
__triggers__ = "ps ";
__authors__ = "マギルゥーベルベット";

# IDEA: get cpu usage and use -1,-2,-3,-4 variants of this icon
iconPath = iconLookup("task-process-0");

commands = commandlib.CommandRegistry();

def initialize():
    global commands;

    for i in [
        {"title": "find",  "desc": "Search for processes"},
        #{"title": "debug", "desc": "Debug command"},
    ]:
        commands.addCommand(commandlib.Command(
            command=i["title"], description=i["desc"],
            completionPrefix=__triggers__, iconPath=iconPath, id=__title__));

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

    if query.command.command == "find":
        for proc in ps.filter_by_query(query.query):
            text = f"{proc['pid']} {proc['command']}";

            # make text italic and add uid when user foreign process
            if proc["owned_by_user"] == False:
                text = f"<i>{text} ({proc['uid']} {ps.get_username_by_uid(proc['uid'])})</i>";

            # TODO: change clipboardText to make it more useful?
            actions = [
                ClipAction(text="Copy to clipboard", clipboardText=f"{text}\n{proc['cmdline']}\n"),
            ];

            # add signal sending actions when process is owned by the current user
            if proc["owned_by_user"] == True:
                def make_sig_action(signum: signal.Signals) -> FuncAction:
                    return FuncAction(
                        text=f"Send {signum.name}",
                        callable=lambda signum=signum, pid=proc["pid"]: ps.send_signal(pid, signum),
                    );

                # create signal actions
                for signum in [
                    signal.SIGINT,
                    signal.SIGTERM,
                    signal.SIGKILL,
                    signal.SIGUSR1,
                    signal.SIGUSR2,
                ]:
                    actions.append(make_sig_action(signum));

            albertItems.append(Item(
                id=__title__,
                icon=iconPath,
                subtext=proc["cmdline"],
                text=text,
                completion=__triggers__,
                urgency=ItemBase.Normal,
                actions=actions,
            ));

    # elif query.command.command == "debug":
    #     albertItems.append(Item(
    #         id=__title__,
    #         icon=iconPath,
    #         subtext="hello world",
    #         text="example text",
    #         urgency=ItemBase.Normal,
    #         actions=[],
    #     ));

    return albertItems;
