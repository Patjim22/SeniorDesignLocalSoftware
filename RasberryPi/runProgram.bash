#!/bin/bash
cd "$(dirname "$(realpath "$0")")"

python3 -u get_scanner.py | python3 MainProgram.py
