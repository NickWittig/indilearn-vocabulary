#!/bin/bash

#linters
.py_env/Scripts/python.exe -m black .
.py_env/Scripts/python.exe -m autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive .  

#checks
.py_env/Scripts/python.exe -m black --check .
.py_env/Scripts/python.exe -m flake8
.py_env/Scripts/python.exe -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
.py_env/Scripts/python.exe -m flake8 . --count --exit-zero --statistics
