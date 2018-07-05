class CommandLineInterfacecException(Exception):
    def __init__(self):
        self.message = "An exception in the command line input parsing occurred"

    def __str__(self):
        return self.message


class InvalidCommandException(CommandLineInterfacecException):
    def __init__(self, command):
        self.message = "The command '" + command + "' is invalid. Please check documentation or use 'help' command"


class MissingArgumentsException(CommandLineInterfacecException):
    def __init__(self, expected_args_number, actual_args):
        self.message = "Not enough arguments. Expected " + expected_args_number + ". Received " + \
                       len(actual_args) + ' , namely ' + actual_args


class InvalidOperatorException(CommandLineInterfacecException):
    def __init__(self, operator):
        self.message = "The operator '" + operator + "' is invalid. Please check documentation or use 'help' command"
