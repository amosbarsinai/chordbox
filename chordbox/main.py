import sys
from . import subcommands
import pathlib
from rich import console
from .core.song import get_songs
from . import error

HELP = """Usage:
    chordbox [-h | --help] [-v | --version] <command> [<args>]
Commands:
  list   [-l | --long] List locally installed songs
  lyrics <SONG>        Print the lyrics of SONG
"""
VERSION = "0.1.0"
CHORDBOX_HOME_DIR = pathlib.Path("~/Music/Chordbox Home").expanduser()

def main():
    if not CHORDBOX_HOME_DIR.exists():
        CHORDBOX_HOME_DIR.mkdir(parents = True)
        (CHORDBOX_HOME_DIR / "Songs").mkdir()

    argv = sys.argv[1:]
    if len(argv) == 0:
        print(HELP)
        return 1

    if argv[0].startswith('-'):
        match argv[0]:
            case '-h' | '--help':
                print(HELP)
                return 0
            case '-v' | '--version':
                print(VERSION)
                return 0
            case _:
                error.error(f"Unexpected option {argv[0]}")
                print(HELP)
                return 1

    # Create a global list of songs
    # For now, the unique identifier of each song will be its absolute path
    # It technically can be relative, but I'm future-proofing it for some point
    # in which I'll implement multi-directory song registries.
    songs = {song.name: song for song in get_songs(CHORDBOX_HOME_DIR / "Songs")}

    rich_console = console.Console()
    command = argv[0]
    result = 0
    match command:
        case "list":
            result = int(not subcommands.list_songs(songs, argv[1:], rich_console))
        case "lyrics":
            result = int(not subcommands.lyrics(songs, argv[1:]))
        case _:
            error.error(f"Unkown subcommand {command}.", file=sys.stderr)
            print(HELP)
            return 1
    return result
