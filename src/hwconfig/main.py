from pathlib import Path

import click
from git import Repo
from result import Err, Ok, Result

from hwconfig.installer.config import InstallerConfig
from hwconfig.installer.copy import CopyInstaller
from hwconfig.installer.protocol import Installer
from hwconfig.installer.terminal import TerminalInstaller
from hwconfig.settings import get_settings
from hwconfig.util import get_powershell_dir, get_win_terminal_config, in_linux, in_windows

# TODO: Implement submit command
# TODO: Test coverage (util module, terminal installer)
# TODO: CLI Tests
# TODO: Documentation pass


def _get_powershell_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "powershell"

    match get_powershell_dir():
        case Ok(v):
            target = v
        case Err(e):
            return Err(f"Could not get powershell dir: {e}")

    installer_config = InstallerConfig(name="powershell", source=source, target=target)

    return Ok(CopyInstaller(config=installer_config))


def _get_terminal_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "terminal" / "settings.json"
    target = get_win_terminal_config()
    installer_config = InstallerConfig(name="terminal", source=source, target=target)

    return Ok(TerminalInstaller(config=installer_config))


def _get_fish_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "fish"
    target = Path.home() / ".config" / "fish"

    installer_config = InstallerConfig(name="fish", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def _get_hyper_installer() -> Result[Installer, str]:
    settings = get_settings()
    source = settings.data_repo_dir / "hyper"
    target = Path.home()

    installer_config = InstallerConfig(name="hyper", source=source, target=target)
    return Ok(CopyInstaller(config=installer_config))


def _get_installers_win() -> Result[list[Installer], str]:
    installers: list[Installer] = []

    for r in (_get_powershell_installer(), _get_terminal_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def _get_installers_linux() -> Result[list[Installer], str]:
    installers: list[Installer] = []

    for r in (_get_fish_installer(), _get_hyper_installer()):
        match r:
            case Ok(v):
                installers.append(v)
            case Err(e):
                return Err(e)

    return Ok(installers)


def get_installers() -> Result[list[Installer], str]:
    if in_windows():
        return _get_installers_win()
    if in_linux():
        return _get_installers_linux()

    return Err("Unsupported platform.")


pass_installers = click.make_pass_decorator(list)


@click.group()
@click.pass_context
def hwconfig(ctx: click.Context) -> None:
    """Hwconfig CLI."""
    match get_installers():
        case Ok(v):
            ctx.obj = v
        case Err(e):
            ctx.fail(message=e)


@hwconfig.command("sync")
def sync_data_repo_command() -> None:
    settings = get_settings()

    if settings.data_repo_dir.exists():
        repo = Repo(settings.data_repo_dir)
        repo.remotes.origin.pull()
    else:
        repo = Repo.clone_from(settings.data_repo_url, settings.data_repo_dir)

    click.echo("Data repo synced.")


@hwconfig.command("list")
@pass_installers
def list_command(installers: list[Installer]) -> None:
    """List available configs."""
    for installer in installers:
        click.echo(installer.config.name)


@hwconfig.command("install")
@pass_installers
def install_command(installers: list[Installer]) -> None:
    """Install config files."""
    for installer in installers:
        match installer.install():
            case Ok(v):
                click.echo(v)
            case Err(e):
                click.echo(f"Error: {e}")


@hwconfig.command("uninstall")
@pass_installers
def uninstall_command(installers: list[Installer]) -> None:
    """Delete installed config files and the local data repo."""
    for installer in installers:
        match installer.uninstall():
            case Ok(v):
                click.echo(v)
            case Err(e):
                click.echo(f"Error: {e}")


@hwconfig.command("submit")
def submit_config_command(_: str) -> None:
    """Copy and submit local config to remote."""
    click.echo("Submit command not implemented yet.")
