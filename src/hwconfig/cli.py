import click

from hwconfig.install import get_installers, update_config_data


@click.group()
def hwconfig() -> None:
    pass


@hwconfig.command()
def install() -> None:
    """Install config files"""
    click.echo("Installing configs...")

    update_config_data()

    for installer in get_installers():
        result = installer()
        click.echo(click.style(result, fg="green"))

    click.echo("Configs installed!")
