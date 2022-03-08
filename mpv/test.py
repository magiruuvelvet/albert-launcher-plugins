import indexer;
import os;

rootdir = os.path.join(os.getenv("HOME"), "ビデオ");
files = indexer.get_all_files(rootdir);

for file in files:
    print(file["path"]);

print(len(files));
