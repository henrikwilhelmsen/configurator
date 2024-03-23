"""configurator: A tool for managing config files."""
from shutil import rmtree

import click
from git import Repo
from result import Err, Ok

from configurator.installer.protocol import Installer
from configurator.installer.setup import get_installers
from configurator.settings import get_settings

# TODO: Test coverage (util module, terminal installer)
# TODO: CLI Tests


def click_echo_success(string: str) -> None:
    """Success formatted `click.echo`.

    Args:
        string: The string to echo.
    """
    click.echo(click.style(string, fg="green"))


def click_echo_error(string: str) -> None:
    """Error formatted `click.echo`.

    Args:
        string: The string to echo.
    """
    click.echo(click.style(string, fg="red"))


def click_echo_warning(string: str) -> None:
    """Warning formatted `click.echo`.

    Args:
        string: The string to echo.
    """
    click.echo(click.style(string, fg="orange"))


@click.group()
def cfg() -> None:
    """configurator: A tool for managing config files."""


@cfg.command("pull")
def pull_data_repo_cmd() -> None:
    """Pull changes from the data repo."""
    settings = get_settings()

    if settings.data_repo_dir.exists():
        repo = Repo(settings.data_repo_dir)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(settings.data_repo_url, settings.data_repo_dir)

    click_echo_success("Data repo synced.")


@cfg.command("push")
@click.argument("message")
@click.option("--dry-run", is_flag=True)
def push_data_repo_cmd(message: str, dry_run: bool) -> None:  # noqa: FBT001
    """Commit and push changes to the data repo."""
    settings = get_settings()

    if not settings.data_repo_dir.exists():
        click_echo_warning("Data repo does not exist. Run `cgf pull` to create it.")
        return

    repo = Repo(settings.data_repo_dir)

    files: list[str] = [item.a_path for item in repo.index.diff(None)]  # type: ignore[partially-unknown-call]
    files.extend(repo.untracked_files)

    if not files:
        click.echo("No changes to push.")
        return

    if not dry_run:
        repo.index.add(files)  # type: ignore[partially-unknown-call]
        repo.index.commit(message)
        repo.remotes.origin.push()

    click_echo_success("\nFiles committed and pushed to data repo:\n")
    for file in files:
        click.echo(f"   {file}")
    click.echo("")


@cfg.command("status")
def status_cmd() -> None:
    """Get the git status of the data repo."""
    settings = get_settings()

    if not settings.data_repo_dir.exists():
        click_echo_warning("Data repo does not exist. Run `cgf pull` to create it.")
        return

    repo = Repo(settings.data_repo_dir)
    repo.git.status()
    click.echo(repo.git.status())


@cfg.command("list")
def list_cmd() -> None:
    """List available configs."""
    match get_installers():
        case Ok(v):
            for installer in v:
                click.echo(installer.config.name)
        case Err(e):
            click_echo_error(f"Failed to list installers: {e}")


@cfg.command("install")
def install_cmd() -> None:
    """Install config files, copying from data repo to local paths."""
    match get_installers():
        case Ok(v):
            installers = v
        case Err(e):
            click_echo_error(f"Failed to get installers: {e}")
            return

    for installer in installers:
        match installer.install():
            case Ok(v):
                click_echo_success(v)
            case Err(e):
                click_echo_error(f"Error: {e}")


@cfg.command("uninstall")
def uninstall_cmd() -> None:
    """Delete installed config files and the local data repo."""
    try:
        settings = get_settings()
        rmtree(settings.data_repo_dir)
        click_echo_success("Data repo removed.")
    except PermissionError as e:
        click_echo_error(f"Failed to remove data repo: {e}")
        return
    except FileNotFoundError as e:
        click_echo_error(f"Data repo not found: {e}")
        return
    except OSError as e:
        click_echo_error(f"Failed to remove data repo: {e}")
        return


@cfg.command("from-local")
@click.argument("configs", nargs=-1)
def from_local_cmd(installers: list[Installer], configs: tuple[str]) -> None:
    """Copy local config files to the data repo."""
    match get_installers():
        case Ok(v):
            installers = v
        case Err(e):
            click_echo_error(f"Failed to get installers: {e}")
            return

    for config in configs:
        for installer in installers:
            if installer.config.name == config:
                match installer.write_to_source():
                    case Ok(v):
                        click_echo_success(v)
                    case Err(e):
                        click_echo_error(f"Error: {e}")


@cfg.command("settings")
def settings_cmd() -> None:
    """View the current settings."""
    click.echo(get_settings().model_dump_json(indent=2))
