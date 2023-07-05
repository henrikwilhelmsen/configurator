"""Module for the hwconfig CLI."""
import click

from hwconfig.install import get_installers, get_sync_config_data_dir


@click.group()
def hwconfig() -> None:
    """Hwconfig CLI."""


@hwconfig.command()
def install() -> None:
    """Sync and install config files."""
    click.echo("Installing config files...")

    config_data_dir = get_sync_config_data_dir()

    for installer in get_installers():
        result = installer(config_data_dir)
        click.echo(click.style(result, fg="green"))

    click.echo("Config files installed!")


@hwconfig.command()
def uninstall() -> None:
    """Uninstall configuration files and revert to the state prior to installation."""
    click.echo("Uninstall not implemented yet!")
