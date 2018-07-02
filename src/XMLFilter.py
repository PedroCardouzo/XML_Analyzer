# filter_xml_tree :: [ConditionalTuple] Element -> Element
# high level description: recieves a list that represents a series of conditions to filter the XML
# low level:
# receives a list of conditions and an Element, it then proceeds to filter the xml as so
# every ConditionalTuple.candidate which contains an ConditionalTuple.field that when applied
# ConditionalTuple.cond(ConditionalTuple.field, ConditionalTuple.value) returns false do not appear on output
# todo: might leave empty tags, so I should do a cleanup function, probably as an option on "indent xml"
def filter_xml_tree(conditions, xml):
    for cond in conditions:
        candidates = xml.findall('.//' + cond.candidate)
        acc = '/..'
        while len(candidates) > 1:
            candidates = xml.findall('.//' + cond.candidate + acc)
            acc += '/..'

        # here we have the higher level element which is unique and contains every occurrence of the cond.candidate
        top_level = candidates[0]
        if top_level is None:
            raise Exception

        for child in xml:
            filter_xml(cond, child, top_level)

    return xml


# filter_xml :: ConditionalTuple Element Element -> None
# side-effects: removes tags that didn't get approved by the logic
# recieves a ConditionalTuple, a xml element and its parent. It then proceeds to
# if the element (2nd argument, sub_xml) is the candidate, it proceeds to validade it,
#           removing itself from the parent Element if condition is not met
# if it is not, it calls the function recursively to its children
def filter_xml(condition, sub_xml, parent):
    if sub_xml.tag == condition.candidate:
        if not make_cond(condition)(sub_xml):
            parent.remove(sub_xml)
    else:
        for child in list(sub_xml):
            filter_xml(condition, child, sub_xml)


def make_cond(cond):
    return lambda x: cond.comp(x.find(".//" + cond.field).text, cond.value)
