#!/usr/bin/bash

me=$(whoami)
cd /home/$me/clickoor-v2

DISPLAY=:0 python3 main.py
