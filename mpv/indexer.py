import os;

def get_all_files(rootdir: str) -> list[str]:
    if (len(rootdir) == 0 or rootdir == '/'):
        raise RuntimeError("Refusing to scan empty path or the entire root filesystem.");
    if not os.path.isdir(rootdir):
        raise RuntimeError(f"Given path is not a directory: {rootdir}");

    fileList = [];
    for root, subdirs, files in os.walk(rootdir, topdown=True):
        # ignore hidden files and folders
        files = [f for f in files if not f[0] == '.'];
        subdirs[:] = [d for d in subdirs if not d[0] == '.'];

        for file in files:
            path = os.path.join(root, file);
            basename = path[len(rootdir)+1:];

            fileList.append(dict(
                path=path,
                nameBase=os.path.basename(os.path.splitext(file)[0]),
                nameFull=basename,
                nameFullLower=basename.lower(),
            ));

    return fileList;
