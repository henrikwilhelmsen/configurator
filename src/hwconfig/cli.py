"""Module for the hwconfig CLI."""
import click


@click.group()
def hwconfig() -> None:
    """Hwconfig CLI."""


@hwconfig.command()
def install() -> None:
    """Sync and install config files."""
    # Check if config exists, if not: stop and ask user to run configure command.
    # Get and run each installers install method from config
    # Echo results
    click.echo("Install command not implemented yet.")


@hwconfig.command()
def uninstall() -> None:
    """Uninstall configuration files and revert to the state prior to installation."""
    # Check if config exists, if not stop and say nothing to uninstall
    # Get and run each installers uninstall method from config
    # Echo results
    click.echo("Uninstall command not implemented yet.")


@hwconfig.command()
def configure() -> None:
    """Set the url of the config data repository."""
    # Create new config from user input
    # Write config to file
    # Echo results
    click.echo("Configure command not implemented yet.")
