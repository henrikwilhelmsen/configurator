# hw-config-cli

Python cli app to manage and install my config files for Windows and Ubuntu.

Config files located in [hw-config-data](https://github.com/henrikwilhelmsen/hw-config-data)

## Installation

### Install Windows dependencies

```PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/henrikwilhelmsen/hw-config-cli/dev/split-data-cli/scripts/bootstrap.ps1" -OutFile "./bootstrap.ps1"; &"./bootstrap.ps1"
```

### Install Ubuntu dependencies

```shell
curl -s https://raw.githubusercontent.com/henrikwilhelmsen/hw-config-cli/dev/split-data-cli/scripts/bootstrap.sh | bash
```

### Config Setup

Install the hwconfig cli with pipx:

```shell
pipx install git+https://github.com/henrikwilhelmsen/hw-config-cli.git@dev/split-data-cli
```

Install the configs:

```shell
hwconfig install
```
