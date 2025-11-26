import pathlib
import tomllib

class Song:
    def __init__(self, path: pathlib.Path, name: str, author: str, album: str, released: int, audio: pathlib.Path, lyrics: pathlib.Path):
        self.path     =     path
        self.name     =     name
        self.author   =   author
        self.album    =    album
        self.released = released
        self.audio    =    audio
        self.lyrics   =   lyrics

    @staticmethod
    def new(source: pathlib.Path):
        if not source.exists():
            return
        if not source.is_file():
            return
        path = source.parent.absolute()
        # read song data
        with open(source, "rb") as songinfo:
            try:
                songinfo = tomllib.load(songinfo)
            except tomllib.TOMLDecodeError:
                return
        if not "songinfo" in songinfo.keys():
            return

        if "name" in songinfo["songinfo"].keys():
            name = songinfo["songinfo"]["name"]
        else:
            name = None

        if "author" in songinfo["songinfo"].keys():
            author = songinfo["songinfo"]["author"]
        else:
            author = None

        if "album" in songinfo["songinfo"].keys():
            album = songinfo["songinfo"]["album"]
        else:
            album = None
        
        if "released" in songinfo["songinfo"].keys():
            released = songinfo["songinfo"]["released"]
        else:
            released = None
        
        if "audio" in songinfo["songinfo"].keys():
            audio = path / pathlib.Path(songinfo["songinfo"]["audio"])
        else:
            audio = None
        
        if "lyrics" in songinfo["songinfo"].keys():
            lyrics = path / pathlib.Path(songinfo["songinfo"]["lyrics"])
        else:
            lyrics = None
        
        return Song(path, name, author, album, released, audio, lyrics)
    
    def __str__(self):
        return self.name if self.name else "<unnamed>"

def get_songs(songs_dir: pathlib.Path) -> list[Song]:
    songs = list()
    for child in songs_dir.iterdir():
        if child.is_dir():
            if (child / "songinfo.toml"):
                song = Song.new(child / "songinfo.toml")
                if song:
                    songs.append(song)
    return songs
