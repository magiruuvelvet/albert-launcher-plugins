import os;

#uid = os.getuid();

def filter_by_query(query: str) -> list:
    if len(query) == 0:
        return [];

    query = query.lower();
    results = [];
    for dir_entry in os.scandir("/proc"):
        try:
            if dir_entry.name.isdigit(): # and dir_entry.stat().st_uid == uid:
                proc_pid = dir_entry.name;
                proc_command = open(os.path.join(dir_entry.path, "comm"), "r").read().strip();
                proc_cmdline = open(os.path.join(dir_entry.path, "cmdline"), "r").read().strip().replace("\0", " ");
                if query in proc_pid or query in proc_command.lower() or query in proc_cmdline.lower():
                    results.append(dict(
                        pid=proc_pid,
                        command=proc_command,
                        cmdline=proc_cmdline,
                    ));
        except FileNotFoundError:
            continue
        except IOError:
            continue
    return results;
