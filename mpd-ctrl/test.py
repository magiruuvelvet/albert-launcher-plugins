import os;
from mpd import MPDClient;

socketFile = os.path.join(os.getenv("HOME"), ".local/share/cantata/mpd/socket");

client = MPDClient();
client.connect(socketFile);

currentsong = client.currentsong();

print(currentsong["artist"]);
print(currentsong["albumartist"]);
print(currentsong["album"]);
print(currentsong["title"]);
print(currentsong);

print(client._command_list);
