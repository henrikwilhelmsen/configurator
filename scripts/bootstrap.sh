#!/bin/bash

# python variables
PYTHON_VERSION=3.11.0
NO_PYTHON=0

# text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# get optional --python-version and --no-python arguments
while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
    --python-version)
        PYTHON_VERSION="$2"
        shift
        shift
        ;;
    --no-python)
        NO_PYTHON=1
        shift
        ;;
    *) # unknown option
        echo "Unknown option: $1"
        exit 1
        ;;
    esac
done

function is_wsl() {
    if [[ $(uname -r) =~ .*microsoft-standard.* ]]; then
        return 0 # WSL, return true
    else
        return 1 # Not WSL, return false
    fi
}

function is_command_installed() {
    if command "$@" >/dev/null 2>&1; then
        return 0 # command succeeded, return true
    else
        return 1 # command failed, return false
    fi
}

function is_package_installed() {
    if dpkg -s "$@" >/dev/null 2>&1; then
        return 0

    else
        return 1
    fi
}

# https://stackoverflow.com/questions/47234947/spinner-animation-and-echo-command
function spinner() {
    local PROC="$1"
    local delay="0.1"
    tput civis # hide cursor
    while [ -d "/proc/$PROC" ]; do
        printf '\033[s\033[u[ / ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ — ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ \ ] %s\033[u' "$str"
        sleep "$delay"
        printf '\033[s\033[u[ | ] %s\033[u' "$str"
        sleep "$delay"
    done
    printf '\033[s\033[u%*s\033[u\033[0m' $((${#str} + 6)) " " # return to normal
    tput cnorm                                                 # restore cursor
    return 0
}

function install_hyper() {
    if is_package_installed hyper; then
        echo -e "Hyper already installed, skipping."
        return 0
    elif is_wsl; then
        echo "In wsl, skipping Hyper installation."
        return 0
    else
        echo "Installing Hyper..."

        function _install_hyper() {
            tmpdir=$(mktemp -d)
            wget -q https://releases.hyper.is/download/deb -O "$tmpdir/hyper.deb"
            sudo apt-get install -y "$tmpdir/hyper.deb"
            sudo rm -rf "$tmpdir"

            # set Hyper as default terminal
            update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator /opt/Hyper/hyper 50
        }

        _install_hyper >/dev/null 2>&1 # Supress command output

        if is_package_installed hyper; then
            echo -e "${GREEN}Hyper installed!${NC}"
            return 0
        else
            echo -e "${RED}Hyper installation failed${NC}"
            return 1
        fi
    fi
}

function install_fish() {
    if is_command_installed fish --version; then
        echo -e "Fish already installed, skipping."
        return 0
    else
        echo "Installing Fish..."

        function _install_fish() {
            sudo apt-add-repository -y ppa:fish-shell/release-3
            sudo apt-get update && sudo apt-get -y install fish

            local fish_config_dir="$HOME/.config/fish"

            # create fish config file if it does not exist
            if [ ! -d "$fish_config_dir" ]; then
                mkdir -p "$fish_config_dir"
            fi
            if [ ! -f "$fish_config_dir/config.fish" ]; then
                touch "$fish_config_dir/config.fish"
            fi

            curl https://raw.githubusercontent.com/oh-my-fish/oh-my-fish/master/bin/install | fish -c ""

            sudo wget https://github.com/JanDeDobbeleer/oh-my-posh/releases/latest/download/posh-linux-amd64 -O /usr/local/bin/oh-my-posh
            sudo chmod +x /usr/local/bin/oh-my-posh

        }

        _install_fish >/dev/null 2>&1 # Supress command output

        if is_command_installed fish --version; then
            echo -e "${GREEN}Fish installed!${NC}"
            return 0
        else
            echo -e "${RED}Fish installation failed, command not found${NC}"
            return 1
        fi
    fi
}

function install_nerd_font() {
    local fonts_dir="$HOME/.local/share/fonts"

    if [ -f "$fonts_dir/Meslo LG M Regular Nerd Font Complete.ttf" ]; then
        echo -e "Meslo nerd-font already installed, skipping."
        return 0
    fi

    echo "Installing Meslo nerd-font..."

    function _install_nerd_font() {
        if [ ! -d "$fonts_dir" ]; then
            mkdir -p "$fonts_dir"
        fi

        if [ ! -f "$fonts_dir/Meslo LG M Regular Nerd Font Complete.ttf" ]; then
            wget "https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Meslo/M/Regular/complete/Meslo%20LG%20M%20Regular%20Nerd%20Font%20Complete.ttf" \
                -O "$fonts_dir/Meslo LG M Regular Nerd Font Complete.ttf"
        fi

        if [ ! -f "$fonts_dir/Meslo LG M Regular Nerd Font Complete Mono.ttf" ]; then
            wget "https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/Meslo/M/Regular/complete/Meslo%20LG%20M%20Regular%20Nerd%20Font%20Complete%20Mono.ttf" \
                -O "$fonts_dir/Meslo LG M Regular Nerd Font Complete Mono.ttf"
        fi
    }

    _install_nerd_font >/dev/null 2>&1 # Supress command output

    if [ -f "$fonts_dir/Meslo LG M Regular Nerd Font Complete Mono.ttf" ]; then
        if [ -f "$fonts_dir/Meslo LG M Regular Nerd Font Complete.ttf" ]; then
            echo -e "${GREEN}Meslo nerd-font installed!${NC}"
            return 0
        fi
    else
        echo -e "${RED}Font installation failed${NC}"
        return 1
    fi
}

function pyenv_configure_bash() {
    local bash_files=(
        "$HOME/.bashrc"
        "$HOME/.profile"
        "$HOME/.bash_profile"
        "$HOME/.bash_login"
    )

    for file in "${bash_files[@]}"; do
        if [ -f "$file" ]; then
            {
                echo 'export PYENV_ROOT="$HOME/.pyenv"'
                echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"'
                echo 'eval "$(pyenv init -)"'
            } >>"$file"
        fi
    done
}

function pyenv_configure_fish() {
    fish -c set -Ux PYENV_ROOT "$HOME/.pyenv"
    fish -c fish_add_path "$PYENV_ROOT/bin"
    echo 'pyenv init - | source' >>"$HOME/.config/fish/config.fish"
}

function install_pyenv() {
    if is_command_installed pyenv --version; then
        echo -e "Pyenv already installed, skipping."
        return 0
    else
        echo "Installing Pyenv..."

        function _install_pyenv() {
            curl https://pyenv.run | bash

            pyenv_configure_bash
            pyenv_configure_fish

            # install Python build dependencies
            sudo apt-get update
            sudo apt-get -y install build-essential libssl-dev zlib1g-dev \
                libbz2-dev libreadline-dev libsqlite3-dev curl \
                libncursesw5-dev xz-utils liblzma-dev libffi-dev
        }

        _install_pyenv >/dev/null 2>&1 # Supress command output

        if is_command_installed pyenv --version; then
            echo -e "${GREEN}Pyenv installed!${NC}"
            return 0
        else
            echo -e "${RED}Pyenv installation failed${NC}"
            return 1
        fi
    fi

}

function install_python() {
    eval "$(pyenv init -)" # needed for the function to reach python installs

    # check that pyenv is installed and available, return 1 if not.
    if ! is_command_installed pyenv --version; then
        echo -e "${RED}Python $PYTHON_VERSION installation failed, pyenv not installed${NC}"
        return 1
    fi

    # install python with pyenv
    if pyenv versions | grep -q "$PYTHON_VERSION"; then
        echo -e "Python $PYTHON_VERSION already installed, skipping."
        return 0
    else
        echo "Installing Python $PYTHON_VERSION..."
        if ! pyenv install "$PYTHON_VERSION"; then # >/dev/null 2>&1
            echo -e "${RED}Python $PYTHON_VERSION installation failed${NC}"
            return 1
        fi
        if ! pyenv global "$PYTHON_VERSION" >/dev/null 2>&1; then
            echo -e "${RED}Failed to set global Python version to $PYTHON_VERSION${NC}"
            return 1
        fi
    fi

    # ensure python version is installed and set
    if python --version | grep -q "$PYTHON_VERSION"; then

        # update pip and setuptools
        if ! python -m pip install --upgrade pip setuptools >/dev/null 2>&1; then
            echo -e "${RED}Failed to upgrade pip and setuptools${NC}"
            return 1
        fi
        # install pipx
        if ! python -m pip install --user pipx >/dev/null 2>&1; then
            echo -e "${RED}Failed to install pipx${NC}"
            return 1
        fi
        # configure pipx
        if ! python -m pipx ensurepath >/dev/null 2>&1; then
            echo -e "${RED}Failed to configure pipx${NC}"
            return 1
        fi

        # install pipenv
        if ! python -m pipx install pipenv >/dev/null 2>&1; then
            echo -e "${RED}Failed to install pipenv${NC}"
            return 1
        fi

        echo -e "${GREEN}Python $PYTHON_VERSION installed and configured!${NC}"
        return 0
    else
        echo -e "${RED}Python $PYTHON_VERSION installation failed${NC}"
        return 1
    fi
}

# Define the install functions to run
install_functions=(
    "install_hyper"
    "install_fish"
    "install_nerd_font"
)

# Conditionally add Python installation commands
if [[ $NO_PYTHON -eq 0 ]]; then
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"

    install_functions+=(
        "install_pyenv"
        "install_python"
    )
fi

# Run the commands in a loop with a spinner
for cmd in "${install_functions[@]}"; do
    $cmd &
    spinner $!
done
