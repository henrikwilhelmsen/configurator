from shutil import rmtree

import click
from git import Repo
from result import Err, Ok

from hwconfig.installer.protocol import Installer
from hwconfig.installer.setup import get_installers
from hwconfig.settings import get_settings

# TODO: Implement submit command
# TODO: Test coverage (util module, terminal installer)
# TODO: CLI Tests
# TODO: Documentation pass
# TODO: Add command for listing application paths (root, data repo, etc.)


@click.group()
def hwconfig() -> None:
    """hw-config-cli: A tool for managing config files."""


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
def list_cmd() -> None:
    """List available configs."""
    match get_installers():
        case Ok(v):
            for installer in v:
                click.echo(installer.config.name)
        case Err(e):
            click.echo(f"Failed to list installers: {e}")


@hwconfig.command("install")
def install_cmd() -> None:
    """Install config files, copying from data repo to local paths."""
    match get_installers():
        case Ok(v):
            installers = v
        case Err(e):
            click.echo(f"Failed to get installers: {e}")
            return

    for installer in installers:
        match installer.install():
            case Ok(v):
                click.echo(v)
            case Err(e):
                click.echo(f"Error: {e}")


@hwconfig.command("uninstall")
def uninstall_cmd() -> None:
    """Delete installed config files and the local data repo."""
    try:
        settings = get_settings()
        rmtree(settings.data_repo_dir)
        click.echo("Data repo removed.")
    except PermissionError as e:
        return click.echo(f"Failed to remove data repo: {e}")
    except FileNotFoundError as e:
        return click.echo(f"Data repo not found: {e}")
    except OSError as e:
        return click.echo(f"Failed to remove data repo: {e}")


@hwconfig.command("from-local")
@click.argument("configs", nargs=-1)
def from_local_cmd(installers: list[Installer], configs: tuple[str]) -> None:
    """Copy local config files to the data repo."""
    match get_installers():
        case Ok(v):
            installers = v
        case Err(e):
            click.echo(f"Failed to get installers: {e}")
            return

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
