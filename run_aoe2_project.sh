#!/usr/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source $PROJECT_DIR/venv/bin/activate
python $PROJECT_DIR/src/main.py --matches-count 1000 --string-tables Y

ret=$?

if [ $ret -ne 0 ]
then
  deactivate
exit 1 # erro
fi

deactivate