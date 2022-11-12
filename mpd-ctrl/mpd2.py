import socket;

class MPD:
    def __init__(self, SOCKET_PATH: str):
        self.SOCKET_PATH = SOCKET_PATH;
        self._mpd_socket = None;
        self.open();

    def __del__(self):
        self.close();

    def open(self):
        self._mpd_socket = socket.socket(socket.AF_UNIX);
        self._mpd_socket.connect(self.SOCKET_PATH);
        #self._mpd_socket.recv(4096);

    def close(self):
        self._mpd_socket.close();

    # send command and receive its response
    def send_command(self, command: str) -> str:
        self._mpd_socket.send(command.encode("utf-8"));
        return self._mpd_socket.recv(4096).decode("utf-8");

    @staticmethod
    def escape_path(path: str) -> str:
        path = path.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n");
        path = "\"" + path + "\"";
        return path;

    def currentsong(self) -> str:
        return self.send_command("currentsong");
