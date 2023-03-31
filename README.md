# hw-terminal-config

Manage and install my personal terminal configurations for Windows and Ubuntu.

## Installation

- Clone the project with Git and open a terminal in the repository folder

### Install Windows dependencies

```PowerShell
scripts\bootstrap.ps1
```

### Install Ubuntu dependencies

```shell
sudo chmod +x ./scripts/bootstrap.sh
./scripts/bootstrap.sh
```

### Config Setup

Install the hwconfig cli with pipx:

```shell
pipx install .
```

Install the configs:

```shell
hwconfig install
```
