#! /usr/bin/env bash
cd "$(dirname "$0")"
python3 -m pip install -r source/requirements.txt
python3 source/main.py
read -n1 -r -p "Press any key to exit."