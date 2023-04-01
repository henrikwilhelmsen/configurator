# hw-config-cli

Python cli app to manage and install my config files for Windows and Ubuntu.

Config files located in [hw-config-data](https://github.com/henrikwilhelmsen/hw-config-data)

## Installation

The cli app requires Python and [pipx](https://pypa.github.io/pipx/), which can be installed manually or with the platform specific bootstrap scripts as described below.

### Install Windows dependencies

```PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/hw-config-cli/scripts/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1"
```

### Install Ubuntu dependencies

```shell
curl -s https://raw.githubusercontent.com/henrikwilhelmsen/hw-config-cli/scripts/bootstrap.sh | bash
```

### CLI and Config Installation

Install the hwconfig cli with pipx:

```shell
pipx install git+https://github.com/henrikwilhelmsen/hw-config-cli.git
```

Install the config files with the cli:

```shell
hwconfig install
```
