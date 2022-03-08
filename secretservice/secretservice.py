import secretstorage;
import subprocess;
from contextlib import closing;

try:
    from albert import critical;
except ImportError:
    pass;

def query(collection: secretstorage.Collection, filter: str) -> list[dict]:
    matches = [];

    items = collection.get_all_items();
    for i in items:
        if filter in i.get_label().lower():
            matches.append({"label": i.get_label(), "item_path": i.item_path});

    return matches;

def get_password(item_path: str) -> str:
    with closing(secretstorage.dbus_init()) as dbus:
        collection = secretstorage.get_default_collection(dbus);
        items = collection.get_all_items();
        for item in items:
            if item_path == item.item_path:
                return item.get_secret();

def copy(item_path: str) -> None:
    try:
        # FIXME: use libX11 or something else, using subprocess for this is disgusting
        p = subprocess.Popen([
            "xclip", "-selection", "clipboard",
        ], stdin=subprocess.PIPE, close_fds=True);
        p.communicate(input=get_password(item_path));

    except OSError as e: # dbus connection lost (get_password) or Popen failed
        critical(str(e));
