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
# TODO: Add command for listing application paths (root, data repo, etc.)


pass_installers = click.make_pass_decorator(list)


@click.group()
@click.pass_context
def hwconfig(ctx: click.Context) -> None:
    """hw-config-cli: A tool for managing config files."""
    match installers():
        case Ok(v):
            ctx.obj = v
        case Err(e):
            ctx.fail(message=e)


@hwconfig.command("pull")
def pull_data_repo_cmd() -> None:
    """Pull changes from the data repo."""
    settings = get_settings()

    if settings.data_repo_dir.exists():
        repo = Repo(settings.data_repo_dir)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(settings.data_repo_url, settings.data_repo_dir)

    click.echo("Data repo synced.")


@hwconfig.command("push")
@click.argument("message")
def push_data_repo_cmd(message: str) -> None:
    """Commit and push changes to the data repo."""
    settings = get_settings()

    if not settings.data_repo_dir.exists():
        click.echo("Data repo does not exist. Run `hwconfig pull` to create it.")
        return

    repo = Repo(settings.data_repo_dir)
    repo.index.add(repo.untracked_files)  # type: ignore[partially-unknown-call]
    repo.index.commit(message)
    repo.remotes.origin.push()

    click.echo("Data repo synced.")


@hwconfig.command("status")
def status_cmd() -> None:
    """Get the git status of the data repo."""
    settings = get_settings()

    if not settings.data_repo_dir.exists():
        click.echo("Data repo does not exist. Run `hwconfig pull` to create it.")
        return

    repo = Repo(settings.data_repo_dir)
    repo.git.status()
    click.echo(repo.git.status())


@hwconfig.command("list")
@pass_installers
def list_cmd(installers: list[Installer]) -> None:
    """List available configs."""
    for installer in installers:
        click.echo(installer.config.name)


@hwconfig.command("install")
@pass_installers
def install_cmd(installers: list[Installer]) -> None:
    """Install config files, copying from data repo to local paths."""
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


@hwconfig.command("from-local")
@click.argument("configs", nargs=-1)
@pass_installers
def from_local_cmd(installers: list[Installer], configs: tuple[str]) -> None:
    """Copy local config files to the data repo."""
    for config in configs:
        for installer in installers:
            if installer.config.name == config:
                match installer.write_to_source():
                    case Ok(v):
                        click.echo(v)
                    case Err(e):
                        click.echo(f"Error: {e}")


@hwconfig.command("settings")
def settings_cmd() -> None:
    """View the current settings."""
    click.echo(get_settings().model_dump_json(indent=2))
