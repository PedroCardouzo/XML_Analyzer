import src.CommandLineInterface as CommandLineInterface
from src.CommandLineInterfaceException import *
from src.XMLExtractorException import *


def main():
    s = None
    while s != "exit":
        try:
            s = input('~: ')
            CommandLineInterface.parse(s)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
