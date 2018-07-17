import CommandLineInterface
import traceback

def main():
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


if __name__ == '__main__':
    main()
