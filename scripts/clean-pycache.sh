#!/usr/bin/env bash

# Run from the project directory

find $path -name '__pycache__' -exec rm -fr {} +
