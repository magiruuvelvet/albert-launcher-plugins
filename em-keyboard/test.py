import em;
import os;

# parse emojis
lookup = em.parse_emojis();
if os.path.isfile(em.CUSTOM_EMOJI_PATH):
    lookup.update(em.parse_emojis(em.CUSTOM_EMOJI_PATH));

# lookup matching emojis
def find(query: str) -> tuple[str, str]:
    query = [query];
    names = tuple(map(em.clean_name, query));
    return em.do_find(lookup, names[0]);

def print_res(found: tuple[str, str]):
    for (name, emoji) in found:
        print(f"{emoji}  {name}");

print_res(find("tears of joy")); # 😂, 😹
print_res(find("rainbow flag")); # 🏳️‍🌈
print_res(find("this should lead to no results"));
