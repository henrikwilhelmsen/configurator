import click
from git import Repo
from result import Err, Ok

from hwconfig.installer.protocol import Installer
from hwconfig.installer.setup import installers
from hwconfig.settings import get_settings

# TODO: Implement submit command
# TODO: Test coverage (util module, terminal installer)
# TODO: CLI Tests
# TODO: Documentation pass


pass_installers = click.make_pass_decorator(list)


@click.group()
@click.pass_context
def hwconfig(ctx: click.Context) -> None:
    """Hwconfig CLI."""
    match installers():
        case Ok(v):
            ctx.obj = v
        case Err(e):
            ctx.fail(message=e)


@hwconfig.command("sync")
def sync_data_repo_cmd() -> None:
    settings = get_settings()

    if settings.data_repo_dir.exists():
        repo = Repo(settings.data_repo_dir)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(settings.data_repo_url, settings.data_repo_dir)

    click.echo("Data repo synced.")


@hwconfig.command("list")
@pass_installers
def list_cmd(installers: list[Installer]) -> None:
    """List available configs."""
    for installer in installers:
        click.echo(installer.config.name)


@hwconfig.command("install")
@pass_installers
def install_cmd(installers: list[Installer]) -> None:
    """Install config files."""
    for installer in installers:
        match installer.install():
            case Ok(v):
                click.echo(v)
            case Err(e):
                click.echo(f"Error: {e}")


@hwconfig.command("uninstall")
@pass_installers
def uninstall_cmd(installers: list[Installer]) -> None:
    """Delete installed config files and the local data repo."""
    for installer in installers:
        match installer.uninstall():
            case Ok(v):
                click.echo(v)
            case Err(e):
                click.echo(f"Error: {e}")


@hwconfig.command("submit")
def submit_cmd(_: str) -> None:
    """Copy and submit local config to remote."""
    click.echo("Submit command not implemented yet.")
