# Cognomen

Cognomen is a tool that automatically generates fictitious names from a list of 422 name generators.
They were all sourced from https://www.fantasynamegenerators.com/ and converted into Python.

# User instructions

1. Git clone the package
   
2. set up your venv
   
3. run this command: pip install -r requirements.txt

4. Open "main_ui.py" and run it. A window will launch. Click on the big question mark symbol for a detailed tutorial.

# Developer instructions - main tool

main_ui.py is the most important script, which launches the actual UI. It actively needs 2 other scripts to function:

converted_functions.py - This is a giant dictionary with all 422 name generators stored as python functions.

master_dict_file.py - This is a verification dictionary that is used to call the right function from converted_functions.py, and also detect corruption in...

# Developer instructions - main tool derivative files

favorite_generators_storage.txt - This file and the 2 listed below are automatically created by main_ui.py. It stores users' favorited name generation functions.

favorite_names_storage.txt - Stores the last 100 generated names that users favorited to save.

user_settings.txt - Currently only remembers whether the user has muted the program or not for future sessions.

# Developer instructions - meta tools

Beyond the above, which constitute the tool itself, there are other meta tools that were used to create the above, the most important of which is...

converter.py - This takes an input of Javascript code and transforms it into usable Python code. It has about a 90% success rate on its first try,
but I had to manually fix the other 10% myself. It sources the original Javascript functions from...

all_js_scripts.py - This is a giant dictionary of 422 Javascript functions taken from the website. They were sourced by using...

get_all_generators.py - This uses Selenium to open every page on fantasynamegenerators.com (for fantasy and real world names, at least, but there are even more I didn't retrieve),
find the Javascript name generation function, and save it into all_js_scripts.py. This led to some encoding errors, fixed by using...

encoding_repair.py - This is a simple script that uses ftfy to fix the corrupted Javascript functions. Essentially, some characters like Ñ, etc. showed up as incomprehensible garbage characters.

name_generator.py - This launches a selenium instance to open a given generator right on the website and retrieve its output. It works, but it's very slow and cumbersome.
This was originally just going to be most of the project, and pretty much everything else in this section was made just to improve upon what this script could do in a much cleaner and faster way.

# Developer instructions - assets

There are 3 sound effects:
1. actionNoise.mp3
2. addNoise.mp3
3. removeNoise.mp3
   
There are 6 images:
1. dragon.png (background image)
2. Logo5.png (Cognomen logo)
3. MuteOffIcon.png (for mute button)
4. MuteOnIcon.png
5. QuestionMark.png (for help button)
6. FrierenIcon.png and .ico (used to create the desktop icon when converting this into a standalone .exe)
