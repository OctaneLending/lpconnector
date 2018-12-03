#!/bin/bash

export VENV_DIR="venv"
export CONFIG_FILE="config.ini"

print_err() {
    tput setaf 1
    echo -e $1
    tput sgr0
}

print_cfm() {
    tput setaf 2
    echo -e $1
    tput sgr0
}

print_msg() {
    tput setaf 3
    echo -e $1
    tput sgr0
}

destroy() {
    print_msg "Destroying entire environment..."
    clean
    clean_venv
    print_cfm "Destruction complete."
}

clean() {
    clean_build
    clean_pyc
}

clean_build() {
    print_msg "Removing build artifacts"
    rm -fr build/
    rm -fr dist/
    rm -fr .eggs/
    rm -fr .idea/
    find . -name '*.egg-info' -exec rm -fr {} +
    find . -name '*.egg' -exec rm -fr {} +
    print_cfm "Done."
}

clean_pyc() {
    print_msg "Removing compiled Python files"
    find . -name '*.pyc' -exec rm -f {} +
    find . -name '*.pyo' -exec rm -f {} +
    find . -name '*~' -exec rm -f {} +
    find . -name '__pycache__' -exec rm -fr {} +
    print_cfm "Done."
}

clean_venv() {
    print_msg "Destroying virtual environment"
    if [[ $VIRTUAL_ENV ]]; then
        deactivate
    fi
    rm -fr $VENV_DIR
    print_cfm "Done."
}

activate() {
    if [ ! -d $VENV_DIR ]; then
        print_err "Virtual environment not present, creating at $VENV_DIR"
        virtualenv $VENV_DIR
    fi
    if [[ -z $VIRTUAL_ENV ]]; then
        print_msg "Activating virtual environment..."
        . $VENV_DIR/bin/activate
    fi
}

config="src/lpconnector/base/config/$CONFIG_FILE"

check_config() {
    if [[ ! -f $config ]]; then
        print_err "No configuration file present, exiting."
        exit 1
    fi
}

config() {
    template="$config.template"

    write_file() {
        while IFS= read -r -u 3 line; do

            if echo $line | grep -Eq "\[[A-Z]+\]"; then
                section=$(echo $line | sed "s/[^A-Z]//g")
                echo "Setting configurations for $section... (Press any key to continue) "
                read -n 1 -s
                echo $line >> $1
            elif [[ -z $line ]]; then
                echo >> $1
            else
                read -sp "$line" input
                echo
                echo $line$input >> $1
            fi

        done 3< $2
    }

    if [[ ! -f $config ]]; then
        print_err "No configuration file present, creating file..."
        touch $config
        write_file $config $template
    else
        read -p "Config file present, do you want to overwrite? [y/n] " -n 1 -r
        echo
        backup="$config.bak"
        cp $config $backup
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_msg "Overwriting config file..."
            > $config
            write_file $config $template
        else
            print_msg "Using config file at $config..."
        fi
    fi
}

check_requirements() {
    if ! which pip > /dev/null; then
        print_err "pip is required to build and run this client\nGo to https://pip.pypa.io/en/stable/installing/ for instructions"
        exit 1
    fi

    if ! pip -q show setuptools; then
        print_err "setuptools is required to build and run this client\nRun \`$ pip install setuptools\` and rerun this script"
        exit 1
    fi

    if ! which virtualenv > /dev/null; then
        print_err "virtualenv is required to build and run this client\nRun \`$ pip install virtualenv\` and rerun this script"
        exit 1
    fi
}

setup() {
    if ! [[ $2 == '--no-clean' ]]; then
        clean
    fi
    print_msg "Running $1 on setup.py"
    python setup.py $1 2> /dev/null
}

build() {
    print_msg "Starting build..."
    if setup build; then
        print_cfm "Build complete."
    else
        print_err "Build failed; exiting."
        exit 1
    fi
}

update() {
    print_msg "Updating lpconnector client..."
    if setup install; then
        print_cfm "lpconnector client updated and ready to use."
    else
        print_err "lpconnector client update failed; exiting."
        exit 1
    fi
}

test() {
    print_msg "Running tests..."
    if setup test; then
        print_cfm "Tests Passed."
    else
        print_err "Tests Failed; exiting."
        exit 1
    fi
}
