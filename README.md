# Chordbox - a local music manager
A work in progress!
To install in a virtual environment:
```bash
git clone https://github.com/AmosBarSinai/chordbox.git
cd chordbox
python3 -m venv .venv
. .venv/bin/activate
pip install poetry
poetry install
```
(Note: you can technically install Chordbox with your system pip if it's not externally managed, but that's not a good idea for now)
To run:
```bash
cd your-chordbox-installation-path
. .venv/bin/activate
poetry run chordbox
```
(Note: you can usually just run `chordbox` if you activated the virtual environment, but this can be less safe if your PATH was altered after running .venv/bin/activate, and doesn't work at all if your the virtualenv's dirname has a space anywhere inside - see [this issue](https://github.com/python-poetry/poetry/issues/3643) for more info.)
