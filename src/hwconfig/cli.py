import click

from hwconfig.install import get_installers, get_sync_config_data_dir


@click.group()
def hwconfig() -> None:
    pass


@hwconfig.command()
def install() -> None:
    """Install config files"""
    click.echo("Installing configs...")

    config_data_dir = get_sync_config_data_dir()

    for installer in get_installers():
        result = installer(config_data_dir)
        click.echo(click.style(result, fg="green"))

    click.echo("Configs installed!")
