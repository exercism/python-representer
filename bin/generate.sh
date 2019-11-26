#! /bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SRC="$( dirname "$DIR" )/src"
export PYTHONPATH="$SRC:$PYTHONPATH"
python bin/generate.py "$@"
