from . import song
from . import error
from os import get_terminal_size

HELP_LISTSONGS = "Usage: chordbox list [-l | --long]"
def list_songs(songs: dict[song.Song], args, rich_console) -> bool:
    songs = songs.values()
    long = False
    if len(args) > 0:
        for arg in args:
            match arg:
                case "-h" | "--help":
                    print(HELP_LISTSONGS)
                    return True
                case "-l" | "--long":
                    long = True
                case _:
                    error.error_subc_unexpected_arg("list", arg)
                    print(HELP_LISTSONGS)
                    return False
    if long:
        for item in songs:
            name = item.name if item.name else "<unnamed>"
            author = item.author if item.author else "Anonymous"
            released = ""
            album = ""
            if item.released:
                released = f" ({item.released})"
            if item.album:
                album = f" from {item.album}"
            rich_console.print(f" - [yellow]{name}[white] by [purple]{author}[green]{released}[pink]{album}")
    else:
        lines: list[str] = list()
        line = ""
        for item in songs:
            if get_terminal_size().columns < len(line + str(item)):
                lines.append(line)
                line = ""
            line += f"{item}  "
        if line:
            lines.append(line)
        del line
        rich_console.print('\n'.join(lines), style="blue bold")
    return True

HELP_LYRICS = "Usage: chordbox lyrics <SONG>"
def lyrics(songs: dict[str, song.Song], args) -> bool:
    if len(args) != 1:
        error.error_subc_args("lyrics", 1, len(args))
        print(HELP_LYRICS)
        return False

    item = args[0]
    if not item in songs:
        error.error(f"Song {item} isn't found in your local music collection.")
        return False
    item = songs[item]
    if item.lyrics == None:
        error.error(f"Song {item} doesn't seem to have any lyrics stored locally.")
        return False
    if not item.lyrics.exists():
        error.error(f"Song {item} exists in your music collection, but its 'lyrics' entry in {item.path / "songinfo.toml"} seems to be misleading. If you added this song manually, try checking for typos.")
        return False
    try:
        with open(item.lyrics, 'r') as lfile:
            lyrics = lfile.read()
    except PermissionError:
        error("For some reason, you don't have permissions to read the lyrics file for this song ({item}).")
        return False
    print(lyrics)
    return True
