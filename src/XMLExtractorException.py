class XMLExtractorException(Exception):
    def __init__(self):
        self.message = "An exception in the XML extraction occurred"

    def __str__(self):
        return self.message


class DuplicateTagInTemplateException(XMLExtractorException):
    def __init__(self, tag):
        self.message = "The tag " + tag + " appears multiple times in the same level of the XML template."


class NotChildOfSameParentException(XMLExtractorException):
    def __init__(self, template_tag, parent_tag):
        self.message = "not all top level elements in the template '" \
                       + template_tag + "' are child of the parent '" + parent_tag + "'"

class NoUniqueRootElementException(XMLExtractorException):
    def __init__(self, top_level_elements):
        self.message = "There are multiple elements in the first level of the xml, namely: " + str(top_level_elements)


class NoCommonParentInTemplateTopLevelException(XMLExtractorException):
    def __init__(self, elements):
        self.message = "The elements '" + str(elements) + "' do not have a common parent"


class NotUniqueTemplateException(XMLExtractorException):
    def __init__(self, template_name):
        self.message = "Template '" + template_name + "' is not unique. Please make sure that template names are unique"


class InnerTemplateNotFoundException(XMLExtractorException):
    def __init__(self, template_name):
        self.message = "Inside template '" + template_name + "' the 'template' tag was not found"


class TemplateNotFoundException(XMLExtractorException):
    def __init__(self, template_name):
        self.message = "The template '" + template_name + "' was not found in the templates file"
