import sys;
import os;
import re;
import unicodedata;
from typing import Union;

script_path = os.path.dirname(os.path.abspath(__file__));
sys.path.insert(0, os.path.join(script_path, "deps/unicode_charnames"));

import unicode_charnames as uc;

REGEX_VALID_QUERY = re.compile(r"^U\+[A-F0-9]{2,}$", re.IGNORECASE);

def uc_valid_query(query: str) -> bool:
    return bool(REGEX_VALID_QUERY.match(query));

def uc_get_name(codepoint: str) -> Union[dict[str, str], None]:
    try:
        character = chr(int(codepoint, 16));
        return dict(char=character, name=unicodedata.name(character));
    except ValueError:
        return None;

def uc_find_by_name(query: str) -> list[dict[str, str]]:
    matches = list(uc.search_charnames(query));
    return list(map(lambda cp: dict(char=chr(int(cp[0], 16)), cp=f"U+{cp[0]}", name=cp[1]), matches));
