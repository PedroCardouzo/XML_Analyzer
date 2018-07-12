import CommandLineInterface as CommandLineInterface
import traceback

def main():
    s = None
    while s != "exit":
        try:
            s = input('~: ')
            CommandLineInterface.parse(s)
        except Exception as e:
            print(traceback.format_exc())
            print(e)


if __name__ == '__main__':
    main()
