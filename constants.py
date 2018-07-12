version = '0.2.1'
base_filepath = "./work_area/"
config_filepath = "./work_area/"
syntax_help = """
# extracts from file using template
extract from <source_file> using <template_file> to <output_file>
:: <source_file> <template_file> <output_file>  # shortcut for the above
# example: extract from in.xml using templ.xml to out.xml
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ templ.xml ------------------
<b>
    <y></y>
</b>
------------------ out.xml ------------------
<b>
    <y>teste</y>
</b>
<b>
    <y>teste2</y>
</b>

# filters from <source_file> the occurrences of <candidate> which do not pass the restraining '<field> <comp> <value>'
filter <source_file> to <output_file> removing <candidate> if <field> <comp> <value> is false
$ <source_file> <output_file> <candidate> <field> <comp> <value>  # shortcut for the above
    where
        <comp> is the comparison operator operator, which can be ==, =, !=, /=, >, >=, <, <=
# example: filter in.xml to out.xml removing b if x != 5 is false
------------------ in.xml ------------------
<root>
    <b>
        <x>5</x>
        <y>teste</y>
    </b>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
------------------ out.xml ------------------
<root>
    <b>
        <x>not5</x>
        <y>teste2</y>
    </b>
</root>
"""