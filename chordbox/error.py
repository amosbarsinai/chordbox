from rich import console
from sys import stderr

error_console = console.Console(file=stderr)

def error(msg: str):
    error_console.print(msg, style="bold red")

def error_subc_args(subcommand: str, expected: tuple[int, int], received: int):
    error(f"Subcommand '{subcommand}' expected {f"{expected[0]} to {expected[1]}" if expected[0] != expected[1] else expected[0]} \
arg{"s" if expected != (1, 1) else ""} (received {received})")

def error_subc_unexpected_arg(subcommand: str, unexpected_arg: str):
    error(f"Subcommand '{subcommand}' received unexpected argument {unexpected_arg}")
