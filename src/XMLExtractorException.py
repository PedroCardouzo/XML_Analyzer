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

class NoUniqueRootElementException:
    def __init__(self, top_level_elements):
        self.message = "There are multiple elements in the first level of the xml, namely: " + str(top_level_elements)


class NoCommonParentInTemplateTopLevelException:
    def __init__(self, elements):
        self.message = "The elements '" + str(elements) + "' do not have a common parent"
