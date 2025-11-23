from rich import console
from sys import stderr

error_console = console.Console(file=stderr)

def error(msg: str):
    error_console.print(msg, style="bold red")

def error_subc_args(subcommand: str, expected: int, received: int):
    error(f"Subcommand '{subcommand}' expected {expected} args (found {received})")

def error_subc_unexpected_arg(subcommand: str, unexpected_arg: str):
    error(f"Subcommand '{subcommand}' received unexpected argument {unexpected_arg}")
