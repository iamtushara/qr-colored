"""Interface for Python CLI Application"""

import logging
from typing import Optional
import typer
from qr_colored import settings


CAPP = typer.Typer()
LOGGER = logging.getLogger()
SETTINGS = settings.load_settings()


@CAPP.command()
def no_op() -> None:
    """performs no operation"""
    typer.echo("no operation performed")
    return None


@CAPP.command()
def write_settings(path: Optional[str] = None) -> None:
    """writes configurable (empty) app settings"""
    outpath = settings.write_settings(path)
    typer.echo(f'Configurable Settings written at: [{outpath}]')


def main():
    """start the CLI application"""
    CAPP()
