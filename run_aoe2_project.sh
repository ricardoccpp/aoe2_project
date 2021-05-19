#!/bin/bash

PROJECT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

source $PROJECT_DIR/venv/bin/activate
python $PROJECT_DIR/src/main.py --matches-count 10 --string-tables Y

ret=$?

if [ $ret -ne 0 ]
then
  deactivate
exit 1 # erro
fi

deactivate