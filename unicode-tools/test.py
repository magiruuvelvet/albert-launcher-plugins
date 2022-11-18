import os;
from pydoc import importfile;
module_path = os.path.realpath(os.path.dirname(__file__));

uc = importfile(module_path + "/lib.py");

print(uc.uc_find_by_name("vertical line"));
print(uc.uc_get_name("0xFFFF"), uc.uc_get_name("0x0020"), uc.uc_get_name("0020"));
print(uc.uc_valid_query("U+001F"), uc.uc_valid_query("U+FFFG"));
