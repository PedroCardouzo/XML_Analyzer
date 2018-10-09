#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
CONFIG_DIR="$DIR""/SAP_XMLs/config.xacfg"
PROGRAM_NAME="$DIR"'/'"Main.py"


usage="xmlint [-h -e -i -f] -- update the integration tool
where:
    -h  show this help text. for app help, call iteractive mode and use help command
    -i  iteractive mode: xmlint -i
    -e  extraction mode: xmlint -e <input_file> <template_name> <output_file>
    -f  filter mode: xmlint -f

"


while getopts 'eifh' OPT; do
  case "$OPT" in
    'e') python3 "$PROGRAM_NAME" "$CONFIG_DIR" "$2" "$3" "$4"
       ;;
    'i') python3 "$PROGRAM_NAME" "$CONFIG_DIR"
       ;;
    'f') python3 "$PROGRAM_NAME" "$CONFIG_DIR" "$2" "$3" "$4" "$5" "$6" "$7"
       ;;
    'h') echo ${usage}
       ;;
    '?') echo "illegal option @ ""$0" >&2
       exit -1
       ;;
  esac
done


