#!/bin/bash
# sync.sh: Wrapper to run the roadmap sync script

if ! command -v python3 &> /dev/null
then
    echo "Python 3 is required but not installed. Aborting."
    exit 1
fi

python3 update_roadmap.py
