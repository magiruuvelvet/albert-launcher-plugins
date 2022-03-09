# mpv

Easily access your videos from Albert launcher.

This plugin has no trigger and always shows results as you type.
Lookup is case insensitive. The `rootDir` string is not included when
searching for files.

## Features

 - Open in mpv (default action)
 - Append to playlist of existing instance (requires `input-ipc-server` to be enabled in mpv)

## Configuration

Stored in `{configLocation()}/mpv/config.yml` (`$HOME/.config/albert/mpv/config.yml`).

```yaml
rootDir: /full/path/to/videos
socketFile: /full/path/to/mpv-ipc-socket
```

Environment variables and `~` (tilde) are **NOT** resolved. A real path must be specified!

Scanning of the entire root directory is not permitted. If you want to do this anyway,
modify `indexer.py` and remove the root filesystem check.

Hidden files and folders (name starting with a dot) are ignored from indexing.
