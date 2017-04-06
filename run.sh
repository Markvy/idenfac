#!/usr/bin/env bash
cd src
python hours.py&
python hosts.py&
python blocked.py&
python resources.py
wait
