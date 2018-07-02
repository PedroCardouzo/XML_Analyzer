class XMLExtractorException(Exception):
    def __init__(self):
        self.message = "An exception in the XML extraction ocurred"

    def __str__(self):
        return self.message


class DuplicateTagInTemplateException(XMLExtractorException):
    def __init__(self, tag):
        self.message = "The tag " + tag + " appears multiple times in the same level of the XML template."


class NotChildOfSameParentException(XMLExtractorException):
    def __init__(self, template_tag, parent_tag):
        self.message = "not all top level elements in the template '" \
                       + template_tag + "' are child of the parent '" + parent_tag + "'"
