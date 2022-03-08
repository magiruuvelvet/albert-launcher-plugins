import secretstorage;
import secretservice;
from contextlib import closing;

try:
    with closing(secretstorage.dbus_init()) as dbus:
        collection = secretstorage.get_default_collection(dbus);

        matches = secretservice.query(collection, "ssh");
        for item in matches:
            print(item["label"], secretservice.get_password(item["item_path"]));

        matches = secretservice.query(collection, "prod");
        for item in matches:
            print(item);

        if len(matches) > 0:
            secretservice.copy(matches[0]["item_path"]);

except Exception as e:
    print(str(e));
