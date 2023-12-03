"""Module for the hwconfig CLI."""
# TODO: style echo based on command result (OK = green, WARNING = orange, ERROR = red)
import click

from hwconfig import main


@click.group()
def hwconfig() -> None:
    """Hwconfig CLI."""


@hwconfig.command()
def install() -> None:
    """Sync and install config files."""
    click.echo(main.install().msg)


@hwconfig.command()
def uninstall() -> None:
    """Uninstall configuration files and revert to the state prior to installation."""
    click.echo(main.uninstall().msg)


@hwconfig.command()
@click.argument("url")
def set_repo(url: str) -> None:
    """Set the url of the config data repository."""
    click.echo(main.set_data_url(url).msg)
