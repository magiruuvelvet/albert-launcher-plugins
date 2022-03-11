from albert import *;
from typing import Union;

class Command:
    def __init__(self,
        command: str,
        description: str,
        completionPrefix: str = "",
        iconPath: str = "",
        id: str = "") -> None:
        self.command: str = command;
        self.description: str = description;
        self.completionPrefix: str = completionPrefix;
        self.iconPath: str = iconPath;
        self.id: str = id;

    def make_help_item(self) -> Item:
        return Item(
            id=self.id, icon=self.iconPath,
            text=self.command, subtext=self.description,
            completion=f"{self.completionPrefix}{self.command} ",
            urgency=ItemBase.Normal, actions=[]);

class MatchedCommand:
    def __init__(self, command: Command, query: str) -> None:
        self.command = command;
        self.query = query;

class CommandRegistry:
    def __init__(self) -> None:
        self.commands: list[Command] = [];

    def addCommand(self, command: Command):
        self.commands.append(command);

    def parse(self, query: str) -> Union[MatchedCommand, str]:
        query = query.strip();

        comm = self.__findCommand(query);
        if comm:
            return comm;
        else:
            return query;

    def __findCommand(self, query: str) -> Union[MatchedCommand, None]:
        for comm in self.commands:
            if query.startswith(comm.command + " "):
                return MatchedCommand(comm, query[len(comm.command)+1:].strip());
        return None;

    def findMatchingCommands(self, query: str) -> list[Item]:
        results = [];
        for comm in self.commands:
            if comm.command.startswith(query):
                results.append(comm.make_help_item());
        return results;

if __name__ == "__main__":
    print("Running tests...");

    registry = CommandRegistry();
    registry.addCommand(Command("help", "this is help"));
    registry.addCommand(Command("test", "test 1"));
    registry.addCommand(Command("abc", "test 2"));

    assert(len(registry.findMatchingCommands("")) == 3);
    assert(len(registry.findMatchingCommands("help")) == 1);
    assert(len(registry.findMatchingCommands("hel")) == 1);
    assert(len(registry.findMatchingCommands("abc")) == 1);
    assert(len(registry.findMatchingCommands("test")) == 1);
    assert(len(registry.findMatchingCommands("test ")) == 0);

    assert(registry.parse("not found") == "not found");
    assert(type(registry.parse("help")) == str);
    assert(type(registry.parse("help ")) == str);
    assert(type(registry.parse("help arg")) == MatchedCommand);
    assert(type(registry.parse("test arg")) == MatchedCommand);
    assert(type(registry.parse("abc arg")) == MatchedCommand);
    assert(type(registry.parse("abc")) == str);
    assert(type(registry.parse("abc ")) == str);

    m: MatchedCommand = registry.parse("help arg");
    assert(m.command.command == "help");
    assert(m.query == "arg");

    m: MatchedCommand = registry.parse("help args ");
    assert(m.command.command == "help");
    assert(m.query == "args");

    m: MatchedCommand = registry.parse("help args a");
    assert(m.command.command == "help");
    assert(m.query == "args a");

    print("DONE!");
