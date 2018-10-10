class XMLAnalyzerException(Exception):
    def __init__(self):
        self.message = "An exception in the command line input parsing occurred"

    def __str__(self):
        return self.message


class InvalidCommandException(XMLAnalyzerException):
    def __init__(self, command):
        self.message = "The command '" + command + "' is invalid. Please check documentation or use 'help' command"


class IncorrectArgumentNumberException(XMLAnalyzerException):
    def __init__(self, expected_args_number, actual_args):
        self.message = "Incorrect argument count. Expected " + str(expected_args_number) + ". Received " + \
                       str(len(actual_args)) + ' , namely ' + str(actual_args)


class InvalidOperatorException(XMLAnalyzerException):
    def __init__(self, operator):
        self.message = "The operator '" + operator + "' is invalid. Please check documentation or use 'help' command"


class InvalidPostProcessTagException(XMLAnalyzerException):
    def __init__(self, post_process_tag):
        self.message = "The post process tag '" + post_process_tag + "' does not exists. Check available tags or " \
                                                                     "implement it in PostProcessing.py function apply"

class InvalidPreProcessTagException(XMLAnalyzerException):
    def __init__(self, pre_process_tag):
        self.message = "The pre process tag '" + pre_process_tag + "' does not exists. Check available tags or " \
                                                                     "implement it in PreProcessing.py function apply"

class TooManyChildrenException(XMLAnalyzerException):
    def __init__(self, tag, children_tag, expected_number):
        self.message = "Too many children nodes in node '" + tag + "'. Expected" + str(expected_number) + ", found " + \
            str(len(children_tag)) + ', namely ' + str(children_tag)

