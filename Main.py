import src.CommandLineInterface as CommandLineInterface
from src.XMLAnalyzerException import *
from src.XMLExtractorException import *
import constants
import sys

import traceback

def main():
    # to test through here:
    sys.argv=['Main.py', '../SAP_XMLs/config.xacfg', '../SAP_XMLs/t_dec.xml', 'legacy-hci-empl-extraction', 'None']

    constants.config_filepath= sys.argv[1] if sys.argv[1] != '' else constants.config_filepath
    actual_arguments = sys.argv[2:]

    if len(actual_arguments) == 0:  # no additional arguments were provided
        s = None
        while s != "exit":
            try:
                s = input('~: ')
                out = CommandLineInterface.parse(s)
                print(out)
            except Exception as e:
                print(traceback.format_exc())
                print(e)

        print('program closed')
    else:
        if len(actual_arguments) == 6:
            out = CommandLineInterface.call_filter(actual_arguments)
        elif len(actual_arguments) == 3:
            out = CommandLineInterface.call_extraction(actual_arguments)
        else:
            raise IncorrectArgumentNumberException('3 for extraction, 6 for filtering', actual_arguments)

        sys.stdout.write(out)


if __name__ == '__main__':
    main()
