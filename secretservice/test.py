import secretstorage;
import secretservice;
from contextlib import closing;

try:
    with closing(secretstorage.dbus_init()) as dbus:
        collection = secretservice.find_collection(dbus, "kbd-launcher");
        collection.unlock();

        print(collection.get_label());

        matches = secretservice.query(collection, "ssh");
        for item in matches:
            print(item["label"], secretservice.get_password(item["item_path"]));

        matches = secretservice.query(collection, "prod");
        for item in matches:
            print(item);

        matches = secretservice.query(collection, "dev");
        if len(matches) > 0:
            print(matches[0]);
            secretservice.copy("kbd-launcher", matches[0]["item_path"]);

except Exception as e:
    print(str(e));
