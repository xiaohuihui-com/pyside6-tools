#!/usr/bin/env bash

python -m nuitka \
        --standalone \
        --windows-console-mode=disable \
        --enable-plugin=pyside6 \
        --nofollow-imports \
        --output-dir=out \
        --show-progress \
        --remove-output \
        main.py