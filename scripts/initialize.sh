#!/bin/bash

if [ ! -d .git ]; then
	echo -e "\033[0;31mNot in project root; exiting.\033[0m"
else
	source scripts/build.sh

	print_msg "Checking requirements (pip, setuptools, virtualenv)..."
	check_requirements
	print_cfm "Necessary packages are installed."
	print_msg "Starting configuration..."
	config
	print_cfm "Config file set."
	print_msg "Setting up virtual environment..."
	activate
	print_cfm "Virtual environment activated."
	print_msg "Building and running tests for lpconnector client..."
	setup test
	read -p "lpconnector client tests complete.  Continue? [y/n] " -n 1 -r
    if [[ REPLY =~ ^[Nn]$ ]]; then
        exit 1
    fi
    echo
	print_msg "Installing lpconnector client..."
	setup install --no-clean
	print_cfm "lpconnector client ready to use!"
fi