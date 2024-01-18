#!/bin/bash

set -ex

echo "[entrypoint.sh] Running with command '$*'";

if [ "$1" = "birthday-paradox" ]; then
    python birthday-paradox/main.py
elif [ "$1" = "prime-finder" ]; then
    python prime-finder/main.py
elif [ "$1" = "tree" ]; then
    python tree/main.py
else
    echo "Unknown command: '$1'";
    echo "Exiting!";
    exit 1;
fi