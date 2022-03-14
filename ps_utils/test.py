from ps import *;

import os;

print(filter_by_query(("discord")));
print(filter_by_query(("kde")));
print(filter_by_query(("systemd")));

is_str = type("") == str;
is_dict = type({}) == dict;

print(is_str, is_dict);

print(get_username_by_uid(os.getuid()));
print(get_username_by_uid(9999)); # non-existend user, return uid as string instead
