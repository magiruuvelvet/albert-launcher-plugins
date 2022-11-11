import os;
import hashlib;
import subprocess;
from queue import Queue;
from threading import Thread
from typing import Union;

def thumbnail(file: str, outputPath: str) -> dict[str, str]:
    md5 = hashlib.sha256(file.encode("utf8")).hexdigest();
    thumbnailPath = f"{outputPath}/{md5}.jpg";
    return dict(thumbnailPath=thumbnailPath, file=file);

def thumbnailWorker(thumbnailQueue: Queue):
    while True:
        thumbnailQueueItem: dict[str, str] = thumbnailQueue.get();
        thumbnailPath = thumbnailQueueItem["thumbnailPath"];
        sourceFile = thumbnailQueueItem["file"];

        if not os.path.exists(thumbnailPath):
            p = subprocess.Popen(["ffmpegthumbnailer", "-i", sourceFile, "-s", "64", "-f", "-o", thumbnailPath],
                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True);
            p.communicate();

        thumbnailQueue.task_done();

def get_all_files(rootdir: str, thumbnailCacheDirectory: Union[str, None] = None) -> list[str]:
    if (len(rootdir) == 0 or rootdir == '/'):
        raise RuntimeError("Refusing to scan empty path or the entire root filesystem.");
    if not os.path.isdir(rootdir):
        raise RuntimeError(f"Given path is not a directory: {rootdir}");

    if thumbnailCacheDirectory != None:
        thumbnailQueue = Queue();
        thumbnailWorkerThread = Thread(target=thumbnailWorker, args=(thumbnailQueue,));
        thumbnailWorkerThread.setDaemon(True);
        thumbnailWorkerThread.start();

    fileList = [];
    for root, subdirs, files in os.walk(rootdir, topdown=True):
        # ignore hidden files and folders
        files = [f for f in files if not f[0] == '.'];
        subdirs[:] = [d for d in subdirs if not d[0] == '.'];

        for file in files:
            path = os.path.join(root, file);
            basename = path[len(rootdir)+1:];

            iconPath = None;
            if thumbnailCacheDirectory != None:
                iconPath = thumbnail(path, thumbnailCacheDirectory);
                thumbnailQueue.put(iconPath);

            fileList.append(dict(
                path=path,
                dir=root,
                nameBase=os.path.basename(os.path.splitext(file)[0]),
                nameFull=basename,
                nameFullLower=basename.lower(),
                iconPath=iconPath["thumbnailPath"] if iconPath != None else None,
            ));

            if thumbnailCacheDirectory != None:
                thumbnailQueue.join();

    return fileList;
