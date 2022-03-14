import os;
import pwd;
import signal;

uid = os.getuid();

def get_username_by_uid(uid: int) -> str:
    try:
        return pwd.getpwuid(uid).pw_name;
    except:
        return str(uid);

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
                    proc_uid = dir_entry.stat().st_uid;
                    results.append(dict(
                        pid=int(proc_pid),
                        command=proc_command,
                        cmdline=proc_cmdline,
                        owned_by_user=proc_uid == uid,
                        uid=proc_uid,
                    ));
        except FileNotFoundError:
            continue
        except IOError:
            continue
    return results;

def send_signal(pid: int, signum: signal.Signals) -> None:
    os.kill(pid, signum);
