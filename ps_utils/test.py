from ps import *;

import enum;

print(filter_by_query(("discord")));
print(filter_by_query(("kde")));
print(filter_by_query(("systemd")));

is_str = type("") == str;
is_dict = type({}) == dict;

print(is_str, is_dict);

class Command(enum.Enum):
    Find = "find";

print(Command.Find.value);
