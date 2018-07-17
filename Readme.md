How to compile:
- on python terminal : run Main.py
- using PyInstaller and creating a single executable:
    place every .py file inside src into main folder (root folder for project)
    alter constants.py to access the folder you desire using the relative path from the executable file.
    run command 'pyinstaller Main.py --onefile'

# How to use
Add templates inside config file
template must follow format

<template_name>
	<template>
		the xml pattern you want to extract here
	</template>
	<config>
		this is optional. doesn't do anything now		
	</config>
</template_name>

* change template_name by the specific template name. this must be unique inside the config.xacfg file
* in constants.py you can change the filepath used to find the config.xacfg file and the other xml files

example of config.xacfg file:

<config>
    <templ1>
        <template>
            <product_info>
                <technical_infotmation>
                    <cpu></cpu>
                    <gpu></gpu>
                    <ram_memory>
			<capacity></capacity>
			<frequency></frequency>
		    </ram_memory>
                </technical_infotmation>
            </product_info>
        </template>

        <config>default</config>
    </templ1>

    <templ2>
 	<name></name>
	<country></country>
	<address>
		<street></street>
		<city></city>
		<number></number>
	</address>
    </templ2>
</config>

Here we have templ1 and templ2, both with config "default" (templ2 gets default config implicitly)
Now lets suppose we have a xml file
in.xml:
<products>
    **lots of tags and stuff**
    <some_tag>
        <some_other_tag>
            <product_info>
                <technical_infotmation>
                    <cpu>
                        <manufacturer>Intel</manufacturer>
                        <model>i5-3570k</model>
                    </cpu>
                    <gpu>
                        <manufacturer>NVidia</manufacturer>
                        <model>GeForce GTX 660Ti</model>
                    </gpu>
                    <ram_memory>
                        <capacity>8 GB</capacity>
                        <manufacturer>Samsung</manufacturer>
                        <frequency>1600 Mhz</frequency>
                        <timing>6-6-6-15</timing>
                    </ram_memory>
                </technical_infotmation>
            </product_info>
            <product_info>
                <technical_infotmation>
                    <cpu>
                        <manufacturer>AMD</manufacturer>
                        <model>Ryzen 7 1700</model>
                    </cpu>
                    <gpu>
                        <manufacturer>AMD</manufacturer>
                        <model>RX 580</model>
                    </gpu>
                    <ram_memory>
                        <capacity>16 GB</capacity>
                        <manufacturer>Corsair</manufacturer>
                        <frequency>1333 Mhz</frequency>
                        <timing>7-7-7-13</timing>
                    </ram_memory>
                </technical_infotmation>
            </product_info>
        </some_other_tag>
    </some_tag>
</products>

and we input command (more about syntax below) "extract from in.xml using templ1 to out.xml"
we should expect out.xml to be like:

out.xml:
<some_other_tag>
    <product_info>
        <technical_infotmation>
            <cpu>
                <manufacturer>Intel</manufacturer>
                <model>i5-3570k</model>
            </cpu>
            <gpu>
                <manufacturer>NVidia</manufacturer>
                <model>GeForce GTX 660Ti</model>
            </gpu>
            <ram_memory>
                <capacity>8 GB</capacity>
                <frequency>1600 Mhz</frequency>
            </ram_memory>
        </technical_infotmation>
    </product_info>
    <product_info>
        <technical_infotmation>
            <cpu>
                <manufacturer>AMD</manufacturer>
                <model>Ryzen 7 1700</model>
            </cpu>
            <gpu>
                <manufacturer>AMD</manufacturer>
                <model>RX 580</model>
            </gpu>
            <ram_memory>
                <capacity>16 GB</capacity>
                <frequency>1333 Mhz</frequency>
            </ram_memory>
        </technical_infotmation>
    </product_info>
</some_other_tag>

* if a template tag is empty, it will take every subtag inside it
* basically you tell the template what you want to extract from the xml file

syntax:

# extracts from file using template
extract from <source_file> using <template_file> to <output_file>
:: <source_file> <template_file> <output_file>  # shortcut for the above
# if <output_file> is exactly None, it will not write to any file and just print the output in the terminal
# example: extract from in.xml using templ1 to out.xml
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
------------------ config.xacfg ------------------
<config>
    <templ1>
        <template>
            <b>
                <y></y>
            </b>
        </template>
        <post_processing>default</post_processing>
    </templ1>
    <templ2>
        <template>
            <tag>another template here</tag>
        </template>
    </templ2>
</config>

(obs.: the chosen template was templ1:
            <b>
                <y></y>
            </b>
------------------ out.xml ------------------
<root>
    <b>
        <y>teste</y>
    </b>
    <b>
        <y>teste2</y>
    </b>
</root>

# filters from <source_file> the occurrences of <candidate> which do not pass the restraining '<field> <comp> <value>'
filter <source_file> to <output_file> keeping <candidate> if <field> <comp> <value>
$ <source_file> <output_file> <candidate> <field> <comp> <value>  # shortcut for the above
    where
        <comp> is the comparison operator operator, which can be ==, =, !=, /=, >, >=, <, <=
# example: filter in.xml to out.xml keeping b if x != 5
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

post_processing:

here you can do things to the xml after the extraction is done. For now, this are the options that you can put inside the post_processing tag:
<filter></filter> | content must have format <candidate> <field> <comp> <value> (same as filter, but without the input and output file names)
                  | if you want the program to ask you each time one of the fields, you can use the $param('') syntax, as following:
                  | Product product_id = $param('input the product id of the products you want to keep: ')
                  | the program will only keep in the xml the tags <Product> where <product_id> content is = to the param provided
                  | when the text prompts 'input the product id of the products you want to keep: ' during the execution
                  | $param is asked to the user at runtime

<text_formatting></text_formatting> | content can be either:
                                    |   'compress' -> to remove spaces, tabs and new lines, compacting XML
                                    |   'indent'   -> to indent the xml for a more human-readable output

* $param(string_to_show_to_user) can be used inside any tag, as long as you don't go over the expected number of arguments
