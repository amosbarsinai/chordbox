from . import song
from . import error
from os import get_terminal_size
import miniaudio

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
        error.error_subc_args("lyrics", (1,1), len(args))
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

HELP_PLAY = "Usage: chordbox play <SONG> [-l | --loop] [-v | --volume VOLUME]"
def play(songs: dict[str, song.Song], args, rich_console) -> bool:
    if len(args) == 0:
        error.error_subc_args("play", (1,4), 0)
        print(HELP_PLAY)
        return False
    loop = False
    volume = 1.0
    songs_to_play: list[song.Song] = list()
    for arg in args:
        match arg:
            case "-h" | "--help":
                print(HELP_PLAY)
                return True
            case "-l" | "--loop":
                loop = True
            case "-v" | "--volume":
                try:
                    volume_index = args.index(arg) + 1
                    volume = float(args[volume_index])
                    if volume < 0.0 or volume > 1.0:
                        raise ValueError()
                except (ValueError, IndexError):
                    error.error("Volume must be a number between 0.0 and 1.0 (inclusive).")
                    print(HELP_PLAY)
                    return False
            case _:
                if arg in songs:
                    songs_to_play.append(songs[arg])
                else:
                    error.error(f"Song {arg} isn't found in your local music collection.")
                    return False
    if len(songs_to_play) == 0:
        error.error("No songs to play were specified.")
        print(HELP_PLAY)
        return False
