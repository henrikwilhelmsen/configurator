import click


@click.group()
def hwconfig() -> None:
    """Hwconfig CLI."""


@hwconfig.command()
def install() -> None:
    """Sync and install config files from remote."""
    click.echo("Install command not implemented yet.")


@hwconfig.command()
def uninstall() -> None:
    """Uninstall configuration files and revert to the state prior to installation."""
    click.echo("Uninstall command not implemented yet.")


@hwconfig.command()
def configure() -> None:
    """Set the url of the config data repository."""
    click.echo("Configure command not implemented yet.")
