# This tool takes a JS script from the fantasy name generator websites and converts it into usable Python
# There are also some testing tools at the bottom to make sure they work as intended


# I don't remember what triple_quoted was used for, but I'm keeping it just in case
from tokenize import triple_quoted
import re
import jsbeautifier
import importlib
from all_js_scripts import script_dict
from master_dict_file import master_keys
import converted_functions
opts = jsbeautifier.default_options()
opts.indent_size = 4


def convert(script, main_index=0):

    # First, check if the generator has already been converted to avoid writing duplicates
    if getattr(converted_functions, f"python_gen{main_index}", False):
        print("Generator already converted.")
        return

    # Beautify the code. I couldn't get this to work without doing this first, because all my "practice scripts"
    # I used to make the foundation for this tool were copied and pasted from Chrome's inspector, and I didn't
    # realize until I was in quite deep that doing so automatically prettified all that script text
    script = jsbeautifier.beautify(script, opts)

    # Names is what the script normally returns, but that name needs to be universal, so other forms are found first and converted
    # It's always found at the end of the js script inside of ".Node(<name>)". Some scripts strangely have both "names" and a variant
    # in the same script that can confuse things, so we just need to identify what it uses as the "main" format of the name return
    # Additionally, this section gives console warnings for unusual scripts that won't automatically convert perfectly
    return_name = re.findall(r".Node\((.*?)\)",script)
    if len(return_name)>=2:
        print(f"Multiple .Nodes detected. {master_keys[main_index]} requires special attention.")
    return_name = return_name[0]

    # The default generator_type is triple because that means it outputs male, female, and neutral names.
    # Even if an unusual generator is a double or quadra/quintuple generator, it's easier to fix it from
    # a baseline of triple than from single
    generator_type = "triple"
    if "nameGen(t" not in script and "nameGen()" not in script:
        print(f"Unusual argument. {master_keys[main_index]} requires special attention.")
    if "tp === 3" in script:
        print(f"More than 3 types detected. {master_keys[main_index]} requires special attention.")
    elif "tp === 2" in script:
        generator_type = "triple"
    elif "tp === 1" in script:
        generator_type = "double"
    else:
        generator_type = "single"

    # The whole script is split and edited line by line, which is fed into the converted_script
    split_string = script.splitlines()
    converted_script = str()
    indent_level = 1

    # Some name generators have only one function, while some have sub functions by gender, which is accounted for with these variables
    function_count = script.count("function ")
    function_count += script.count("function(")
    in_sub_function = False
    in_sub_function_indent = 0
    in_redundancy_section = False
    in_redundancy_section_indent = 0
    # Wraps everything in a larger function with a universal naming convention, so that all several hundred can be reference easily
    converted_script += f"# {master_keys[main_index]}\n"
    converted_script += f"def python_gen{main_index}():\n"
    converted_script += f"\t{return_name} = []\n"


    #This is the conversion script's main logic loop, iterating over every line
    for index, i in enumerate(split_string):
        # Remove existing indents then set them properly
        i = i.strip("\t\n ")
        i = ("\t"*indent_level + i)

        # Bracket replacements and indent logic
        if "{" in i or "}" in i:
            if "{" in i and "}" in i:
                if re.findall(r'\{(.*?)}', i):
                    raise TypeError("Curly list =(")
            if "{" in i:
                i = i.replace(" {", "{")
                i = i.replace("{", "")
                indent_level += 1
            if "}" in i:
                i = i.replace("} ", "}")
                # Below 2 lines are necessary because indent_level generally tells the NEXT line how much
                # to indent, but sometimes it needs to be immediate, as when } starts the sentence
                if i.strip().startswith("}"):
                    i = i[1:]
                i = i.replace("}", "")
                indent_level -= 1

        # Sub function detection logic
        if in_sub_function:
            if in_sub_function_indent == indent_level:
                in_sub_function = False
                indent_level -= 1

        # Redundant section detection logic (such as swear filters)
        if in_redundancy_section:
            if in_redundancy_section_indent < indent_level:
                continue
            in_redundancy_section = False

        # Specific replacements, which ignore or finalize the whole line
        ilower = i.lower()
        if "check." in ilower or "swear." in ilower or  "curse." in ilower or "profanity." in ilower:
            in_redundancy_section = True
            in_redundancy_section_indent = indent_level
            continue
        if "element." in ilower or "document." in ilower or ".css" in ilower or "testswear" in ilower or "br = """ in ilower or ".splice" in ilower:
            continue
        if "++" in i:
            converted_script += "\t"*(indent_level - 1) + "for i in range(10):\n"
            continue

        # General replacements
        if ";" in i:
            i = i.replace(";", "")
        if "function " in i or "function(" in i:
            # If "function" is the whole line, it puts it at the beginning of the next i
            # Then (or otherwise), it changes it to def and puts a colon at the end
            if " " not in i:
                split_string[index+1] = i + " " + split_string[index+1]
                continue
            # Function has two format possibilities for JS, both of which are accounted for here
            if "function " in i:
                i = i.replace("function", "def") + ":"
            if "function(" in i:
                i = i.replace("function", "def") + ":"
                i = i.replace("(", "")
                i = i.replace(")", "")
        # Some things like "var" or "if" could realistically just be part of longer words or
        # be syllables for names, so I use i.split() to make sure they're only deleted if
        # they are at the beginning of the line. I don't want to use i.split() for every single
        # i by default because it seems computationally excessive, so it's only included in edge cases
        if "var" in i:
            if "var" in i.split()[0]:
                i = i.replace("var ", "")
                i = i.replace("var", "")
        # If empty, don't add to converted_script
        if not i.strip():
            continue
        if "===" in i:
            i = i.replace("===", "==")
        if "while" in i:
            # Rarely a name in a list will contain while, else, or if,
            # so we check there aren't quotes in the first word of the line
            # if "while" in i.split()[0]:
            if '"' not in i.strip()[0] and "[" not in i.strip()[0]:
                i += ":"
                if "while " not in i:
                    i = i.replace("while", "while ")
        if "else if" in i:
            i = i.replace("else if", "elif")
        if "if" in i:
            if "if" in i.split()[0]:
            # if '"' not in i.strip()[0] and "[" not in i.strip()[0]:
                i += ":"
        if "else" in i:
            if "else" in i.split()[0]:
            # if '"' not in i.strip()[0] and "[" not in i.strip()[0]:
                i += ":"
        if "||" in i:
            i = i.replace("||", "or")
        if "&&" in i:
            i = i.replace("&&", "and")
        if "!" in i:
            i = i.replace("!", "not")

        # Specific and complex replacements

        # This converts Javascript's random function to a Python equivalent, which requires import random
        if ".length" in i:
            i = re.sub(r'([\w\[\]]+)\.length', r'len(\1)', i)

        if "Math." in i:
            replace = re.findall(r"(Math\..*)", i)
            source = re.findall(r"\*\s+(.*?\)?)[\s);|]", i)
            for p, p2 in zip(replace, source):
                # Whether p2 is a lone number or a variable rnd derived from the length of an array
                # is important to setting up the index inclusivity properly
                if p2.isdigit():
                    i = i.replace(p, f"random.randint(0,{p2})")
                else:
                    i = i.replace(p, f"random.randint(0,{p2}-1)")

        # Figures out if a newly renamed def is the main or sub function
        if "def " in i:
            if "def" in i.split()[0]:
                if "def nameGen" in i:
                    indent_level -= 1
                    continue

                # Subfunctions are indented on the same level as the main in JS, so that is adjusted here
                elif function_count > 1:
                    in_sub_function = True
                    indent_level +=1
                    i = "\t" + i
                    in_sub_function_indent = indent_level - 1

        # Adds the entry to the names list
        if f"{return_name} =" in i or f"{return_name}=" in i:
            if return_name in i.split()[0]:
                i = i.replace(f"{return_name} = ", f"{return_name}=")
                i = i.replace(f"{return_name} =", f"{return_name}=")
                i = i.replace(f"{return_name}=", f"{return_name}.append(better_title(")
                i += "))"

        # Finally, add a line break and add to converted_script
        i = i + "\n"
        converted_script += i

    # If there are sub-functions, this section reorders them so that they're in the right place
    reorder = converted_script.splitlines()
    if function_count > 1:
        sub_function_line = 0
        end_of_variables_line = 0
        for index, i in enumerate(reorder):
            if "def " in i:
                # Ignore the two first main functions
                if index > 1:
                    sub_function_line = index
                    break
            if "for i in range(10):" in i:
                end_of_variables_line = index
        # Reset the converted_script to be empty, then put the lines back in the correct order from reorder variable
        converted_script = str()
        for i in reorder[:end_of_variables_line]:
            converted_script += i + "\n"
        converted_script += "\n\tdef nameGen(type=0):\n"
        for i in reorder[sub_function_line:]:
            converted_script += f"\t{i}\n"
        for i in reorder[end_of_variables_line:sub_function_line]:
            converted_script += f"\t{i}\n"

    # If there aren't sub-functions, a simpler version of reorganizing is still needed to shove in the line
    # "\n\tdef nameGen(type=0):\n" both after the variables are defined and before the logic that it should
    # encapsulate, since Javascript can read the whole page without freaking out about the order of declarations
    else:
        converted_script = str()
        for index, i in enumerate(reorder):
            if "for i in range(10):" in i:
                end_of_variables_line = index
                break
        for i in reorder[:end_of_variables_line]:
            converted_script += i + "\n"
        converted_script += "\n\tdef nameGen(tp=0):\n"
        for i in reorder[end_of_variables_line:]:
            converted_script += f"\t{i}\n"

    # Properly sets up the generator to return 30, 20, or 10 names depending on whether it's a neutral/masculine/feminine
    # generator, a masculine/feminine generator, or just a neutral generator. The main UI is smart enough to discern where
    # to put the results depending on how many it receives.
    if generator_type == "triple":
        converted_script += "\tfor i in range(3):\n"
        converted_script += "\t\tnameGen(i)\n"
    if generator_type == "double":
        converted_script += "\tfor i in range(2):\n"
        converted_script += "\t\tnameGen(i)\n"
    if generator_type == "single":
        converted_script += "\tnameGen()\n"

    converted_script += "\t" + f"return {return_name}"
    with open('converted_functions.py', 'a', encoding ="utf-8") as f:
        f.write("\n" + converted_script + "\n")

    # Tests the function once in the console
    importlib.reload(converted_functions)
    func_name = f"python_gen{main_index}"
    result = getattr(converted_functions, func_name)()
    print(master_keys[main_index])
    print(result)



# These 2 functions are just simpler ways of calling the above function using different criteria

def index_convert(index, endindex=None):
    if endindex is None:
        endindex = index
    for i in range(index, endindex+1):
        convert(script_dict[master_keys[i]], i)

def name_convert(name):
    convert(script_dict[name], master_keys.index(name))



# These 2 are robust testing functions to make sure a generator works as intended

# This one can actually flag false negatives, which is fine. I'm not sure of a better way than searching
# for tp === variants to determine what it's supposed to be without looking at it myself. Bandit Names
# is an example of one that this tester function thinks is supposed to be a single output, but is
# correctly coded as a triple output
def check_enough_names(index):
    original_js = script_dict[master_keys[index]]
    # Bluecap and Knight Names are the only two generators with more than 3 outputs on the website, and I've
    # already made sure they work properly manually
    if "tp === 3" in original_js or "tp===3" in original_js or "tp=== 3" in original_js or "tp ===3" in original_js:
        print(f"bluecap/knights: {master_keys[index]}")
        return
    elif "tp === 2" in original_js or "tp===2" in original_js or "tp=== 2" in original_js or "tp ===2" in original_js:
        correct_amount = 30
    elif "tp === 1" in original_js or "tp===1" in original_js or "tp=== 1" in original_js or "tp ===1" in original_js:
        correct_amount = 20
    else:
        correct_amount = 10

    func_name = f"python_gen{index}"
    result = getattr(converted_functions, func_name)()

    if len(result) != correct_amount:
        print(f"Error: got {len(result)}, expected {correct_amount}, from {func_name}")
        quit()

# The master tester which makes sure a function(s) works without crashing
# 100 times, and checks that it returns the correct amount of total names
def check_enough_names_many(start, end=0):
    if end == 0:
        end = start
    for i in range(start, end+1):
        for p in range(100):
            check_enough_names(i)
        func_name = f"python_gen{i}"
        print(f"{func_name} working as intended")


check_enough_names_many(400, 500)


# Call the main function
# index_convert(2)

# Test amount of names of converted function. 10 = always neutral, 20 = male/female, 30 = male/female/neutral
# print(len(converted_functions.python_gen197()))

# Test converted functions and find their name by index or name
# print(converted_functions.python_gen11())
# print(master_keys[20])
# print(master_keys.index("Twin Names"))