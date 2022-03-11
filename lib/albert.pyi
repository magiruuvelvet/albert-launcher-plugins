###
### Native stubs for Albert Python Extension Interface
### https://github.com/albertlauncher/plugins/tree/master/python
###

from enum import Enum;
from typing import Union;

# Optional [string]. The docstring of the module is used as description of the extension.
# This string will be displayed to the user.
__doc__: str;

# MANDATORY [string]. This variable should hold the pretty name of the extension.
# This string will be displayed to the user.
__title__: str;

# MANDATORY [string].
__version__: str;

# Optional [string, list of strings]. If this extension should be run exclusively,
# this variable has to hold the trigger that causes the extension to be executed.
__triggers__: Union[str, list[str]];

# Optional [string, list of strings]. This variable should hold the name of the author of the extension.
__authors__: Union[str, list[str]];

# Optional [string, list of strings]. This string should contain any dependencies the extension needs to be used.
# The name of the dependency has to match the name of the executable in $PATH.
__exec_deps__: Union[str, list[str]];

# Optional [string, list of strings]. This string should contain any dependencies the extension needs to be used.
# The name of the dependency has to match the name of the package in the PyPI.
__py_deps__: Union[str, list[str]];

# def handleQuery(query: Query) -> list[Item]:
#     """
#     MANDATORY. This is the crucial part of a Python module. When the user types a query,
#     this function is called with a query object representing the current query execution.
#     This function should return a list of Item objects. See the Item class section below.
#     """

# def initialize() -> None:
#     """
#     Optional. This function is called when the extension is loaded. Although you could technically
#     run your initialization code in global scope, it is recommended to initialize your extension
#     in this function. If your extension fails to initialize you can raise exceptions here, which are displayed to the user.
#     """

# def finalize() -> None:
#     """Optional. This function is called when the extension is unloaded."""

class Query:
    """
    The query class represents a query execution. It holds the necessary information to handle a Query.
    It is passed to the handleQuery function. It holds the following read-only properties.
    """

    # This is the actual query string without the trigger. If the query is not triggered this string equals rawstring.
    string: str;

    # This is the full query string including the trigger. If the query is not triggered this string equals string.
    rawString: str;

    # Indicates that this query has been triggered.
    isTriggered: bool;

    def disableSort() -> None:
        """Disables sorting of result items. Preserving the order of insertion."""

class ActionBase:
    pass;

class ClipAction(ActionBase):
    """This class copies the given text to the clipboard on activation."""
    def __init__(self, text: str, clipboardText: str) -> None: ...

class UrlAction(ActionBase):
    """This class opens the given URL with the systems default URL handler for the scheme of the URL on activation."""
    def __init__(self, text: str, url: str) -> None: ...

class ProcAction(ActionBase):
    """This class executes the given commandline as a detached process on activation. Optionally the working directory of the process can be set."""
    def __init__(self, text: str, commandline: list[str], cwd: str = None) -> None: ...

class TermAction(ActionBase):
    """This class executes the given commandline in the terminal set in the preferences. Optionally the working directory of the process can be set."""
    def __init__(self, text: str, commandline: list[str], cwd: str = None) -> None: ...

class FuncAction(ActionBase):
    """This class is a general purpose action. On activation the callable is executed."""
    def __init__(self, text: str, callable: callable = lambda: None) -> None: ...

class ItemBase:
    class Urgency(Enum):
        Normal = None;
        Alert = None;
        Notification = None;
    Normal = Urgency.Normal;
    Alert = Urgency.Alert;
    Notification = Urgency.Notification;

class Item(ItemBase):
    def __init__(self,
        id: str,        # The identifier string of the item. It is used for ranking algorithms and should not be empty.
        icon: str,      # The path of the icon displayed in the item.
        text: str,      # The primary text of the item.
        subtext: str,   # The secondary text of the item. This text should have informative character.

        # The completion string of the item. This string will be used to replace the input line
        # when the user hits the Tab key on an item. Note that the semantics may vary depending on the context.
        completion: str,

        # The urgency of the item. Note that the Urgency enum is defined in the ItemBase class. See the Urgency enum.
        urgency: ItemBase.Urgency,

        # The actions of the item.
        actions: list[ActionBase],
    ) -> None:
        self.id = id;
        self.icon = icon;
        self.text = text;
        self.subtext = subtext;
        self.completion = completion;
        self.urgency = urgency;
        self.actions = actions;

    def addAction(action: ActionBase) -> None:
        """Add an action to the item."""

def debug(obj) -> None: ...
def info(obj) -> None: ...
def warning(obj) -> None: ...
def critical(obj) -> None: ...

def iconLookup(iconName: Union[str, list[str]]) -> str:
    """Perform xdg icon lookup and return a path. Empty if nothing found."""

def cacheLocation() -> str:
    """$HOME/.cache/albert/"""
def configLocation() -> str:
    """$HOME/.config/albert/"""
def dataLocation() -> str:
    """$HOME/.local/share/albert/"""
