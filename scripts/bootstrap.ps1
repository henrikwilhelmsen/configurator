<#
.SYNOPSIS
    This script installs PowerShell, Windows Terminal, Python and Meslo-NF nerd-font
    on Windows using Winget and Scoop package managers.

.PARAMETER pythonVersion
    The version of Python to install. Default is "3.11". Only supports major version numbers.
    See "winget search Python.Python" for available versions.

.NOTES
    - This script requires Winget package manager.
#>

param (
    [string]$pythonVersion = "3.11"
)
function CommandInstalled {
    [CmdletBinding()]
    param (
        [string]$CommandName
    )

    $command = Get-Command $CommandName -ErrorAction SilentlyContinue
    if ($command) {
        return $true
    }
    else {
        return $false
    }
}

function Install-PowerShell {
    if ((CommandInstalled pwsh)) {
        Write-Host "PowerShell already installed, skipping."
        return
    }

    Write-Host "Installing PowerShell..."

    try {
        winget install Microsoft.PowerShell --silent
        Write-Host "Powershell installed!"
    }
    catch {
        Write-Warning "Failed to install PowerShell. Please install it manually."
        return
    }
}
function Install-WindowsTerminal {
    if ((CommandInstalled wt)) {
        Write-Host "Windows Terminal already installed, skipping."
        return
    }
    
    Write-Host "Installing Windows Terminal..."
    
    try {
        winget install Microsoft.WindowsTerminal --silent
        Write-Host "Windows Terminal installed!"
    }
    catch {
        Write-Warning "Failed to install Windows Terminal. Please install it manually."
        return
    }
}

function Install-Python {
    param (
        [string]$pythonVersion
    )

    if (py --list | Select-String -Pattern $pythonVersion -Quiet) {
        Write-Host "Python $pythonVersion already installed, skipping."
        return
    }

    Write-Host "Installing Python $pythonVersion..."

    try {
        winget install Python.Python.$pythonVersion --silent --force
        Write-Host "Python $pythonVersion installed!"
    }
    catch {
        Write-Warning "Failed to install Python $pythonVersion. Please install it manually."
        return
    }
}

function Install-Scoop {
    if ((CommandInstalled scoop)) {
        Write-Host "Scoop already installed, skipping."
        return
    }
    try {
        Invoke-RestMethod get.scoop.sh | Invoke-Expression
    }
    catch {
        Write-Warning "Failed to install Scoop. Please install it manually from https://scoop.sh/."
        return
    }
}

function Install-MesloNFNerdFont {
    # check if Scoop is available, try to install it if not.
    if (!(CommandInstalled scoop)) {
        try {
            Install-Scoop
        }
        catch {
            Write-Warning "Failed to install Scoop, unable to continue font installation."
            return
        }
    }
    
    # check if the font is installed already and return early if it is
    $installedFonts = Get-ChildItem "C:\\\WINDOWS\FONTS" | Select-Object -ExpandProperty Name

    if ($installedFonts -contains "Meslo LG M Regular Nerd Font Complete Windows Compatible.ttf") {
        Write-Host "Meslo-NF already installed, skipping."
        return
    }
    
    # add the nerd-fonts bucket to Scoop if it doesn't exist
    if (!(scoop bucket list | Select-String -Quiet "nerd-fonts")) {
        Write-Host "nerd-fonts bucket missing, adding..."

        try {
            scoop bucket add nerd-fonts
        }
        catch {
            Write-Warning "Failed to add nerd-font bucket to Scoop, unable to continue font installation."
            return
        }
        Write-Host "nerd-fonts bucket added!"
    }

    # install scoop sudo if not available
    if (!(Get-Command sudo -ErrorAction SilentlyContinue)) {
        Write-Host "Scoop sudo not found, installing..."
        
        try {
            scoop install sudo
        }
        catch {
            Write-Warning "Failed to install Scoop sudo, unable to continue font installation."
            return
        }
        Write-Host "Scoop sudo installed!"
    }
    else {
        Write-Host "sudo found, continuing"
    }
    
    # install Meslo-NF with sudo
    try {
        sudo scoop install -g Meslo-NF
    }
    catch {
        Write-Warning "Failed to install Meslo-NF with Scoop."
    }
    
}

#TODO: Add Python setup function - install pipx and pipenv

function BootStrap {
    Install-PowerShell
    Install-WindowsTerminal
    Install-Python -pythonVersion $pythonVersion
    Install-Scoop
    Install-MesloNFNerdFont
}

BootStrap