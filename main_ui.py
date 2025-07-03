import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import webbrowser
from master_dict_file import master_keys
import name_generator
import converted_functions

# This tool creates a UI that lets users use 422 name generators, and save favorite generators
# and favorite names that persist across sessions.

# Main window
window = tk.Tk()
window.title("Cognomen")
window.geometry('1500x800')
# window.tk.call('tk', 'scaling', 3)

# Background section

# The entire reason this whole section exists is just to make the mute button have
# a transparent background. This whole thing was about 6 lines before and worked fine,
# aside from the lack of transparency. The background works better with .place instead
# of .pack like everything else, because it doesn't need to compete for space and
# it's fine (optimal, really) when it's obscured by the other widgets.

# Background image setup
original_background = Image.open("dragon.png")
dragon = ImageTk.PhotoImage(original_background)
bg_frame = tk.Frame(master=window)
bg_frame.place(x=0, y=0, relwidth=1, relheight=1)
canvas = Canvas(bg_frame)
canvas.place(x=0, y=0, relwidth=1, relheight=1)
bg_image = canvas.create_image(750, 400, image=dragon, anchor='center')

title_source = Image.open("Logo5.png")
title = ImageTk.PhotoImage(title_source)
title_place = canvas.create_image(750, 50, image=title, anchor='center')

# This resizing certainly isn't perfect and is magic number special cased
# to this particular image, but it works and that's good enough
def resize_bg(event):
    new_width, new_height = event.width, event.height
    # 17/30 is the ratio of the starting resolution to the background image's width
    # Scaling the height doesn't matter as much, as long as it isn't distorted to begin with
    resized = original_background.resize((int(new_width * (20 / 30)), new_height))
    photo = ImageTk.PhotoImage(resized)
    canvas.image = photo
    canvas.itemconfig(bg_image, image=photo)
    canvas.coords(bg_image, event.width//2, event.height//2)
    canvas.coords(title_place, event.width//2, 50)

canvas.bind("<Configure>", resize_bg)


# Sound effects section

# Grabs previous user mute setting, or creates it if it doesn't exist
try:
    with open("user_settings.txt") as f:
       mute = f.read()
       if "True" in mute:
          mute = [True]
       else:
          mute = [False]
except:
    with open('user_settings.txt', 'w', encoding="utf-8") as f:
        f.write("False")
        mute = [False]

pygame.mixer.init()
muteoff = PhotoImage(file="MuteOff.png").subsample(4,4)
muteon = PhotoImage(file="MuteOn.png").subsample(4,4)

# Mute button will stop existing sounds and prevent future ones
def mute_toggle(mute_list):
    mute_list[0] = not mute_list[0]
    if mute_list[0]:
        pygame.mixer.music.stop()
        canvas.itemconfig(mute_icon, image=muteon)
    else:
        canvas.itemconfig(mute_icon, image=muteoff)
    with open('user_settings.txt', 'w', encoding ="utf-8") as f:
      f.write(str(mute_list[0]))

# Plays a sound effect when called. There are 3 total sound effects:
# Add, remove, and use
def play_sound(soundEffect):
    if not mute[0]:
        pygame.mixer.music.load(f"{soundEffect}.mp3")
        pygame.mixer.music.play()

# This isn't coded as a button, but it is effectively a button
# It's a mute button, and it will not move or resize no matter what
# The resolution is changed to
if not mute[0]:
    mute_icon = canvas.create_image(390, 100, image=muteoff, anchor="nw")
else:
    mute_icon = canvas.create_image(390, 100, image=muteon, anchor="nw")

tag_name = "rect"
rect = canvas.create_rectangle(390, 100, 530, 240, outline="", fill="", tag="rect")



# Help button
help = PhotoImage(file="QuestionMark.png")
help_icon = canvas.create_image(390, 240, image=help, anchor="nw")
tag_name2 = "rect2"
rect2 = canvas.create_rectangle(390, 240, 530, 380, outline="", fill="", tag="rect2")

help_message = ''' Welcome to the Cognomen Naming Tool: powered by https://www.fantasynamegenerators.com/.
Be sure to support the main website, which has even more name generators than the ones found here.

The large list on the bottom of the screen contains 422 unique name generators - simply click on one to use it.
There are generators for any fantasy race/class you can imagine, as well as real world names like Filipino or Basque
names. Click the golden search bar right above it to find one you're looking for, or just peruse until you see
one that looks cool. You can also right click on a generator to save it as a favorite.

Names will populate in the three righthand boxes - neutral names in the purple box, feminine ones in the pink
box, and masculine ones in the blue box. You can click on a name you like to save it in the recent favorite names
box, which is green and located in the bottom left corner of the window. It will save the last 100 favorited names.

The orange box in the top left corner of the window is your favorite generators box. You can run them by left clicking,
or you can right click to remove one from your favorites list. If this is your first time using this tool, some
universally good ones have been curated for you to start off.

There are two buttons located to the right of the orange favorites box - the mute button, which is pointless because
why would anyone ever use that, and the help button (which you probably already know the function of.)

Happy naming =)'''

def open_popup():
   top= Toplevel(window)
   top.geometry("1300x600")
   top.title("Help Window")
   Label(top, text= help_message, justify="center", font=("", 16)).place(x=100,y=60)

# These functions just make sure the above buttons make the cursor change when hovering,
# to communicate functionality even without clicking first
def check_hand_enter():
    canvas.config(cursor="hand2")

def check_hand_leave():
    canvas.config(cursor="")

canvas.tag_bind(tag_name, "<Enter>", lambda event: check_hand_enter())
canvas.tag_bind(tag_name, "<Leave>", lambda event: check_hand_leave())
canvas.tag_bind(tag_name2, "<Enter>", lambda event: check_hand_enter())
canvas.tag_bind(tag_name2, "<Leave>", lambda event: check_hand_leave())
canvas.tag_bind(tag_name2, "<Button-1>", lambda event: open_popup())



# Listboxes section

# Universal options for all listboxes
options = {"font":("Helvetica", 16), "width":30}

# Frame for names listbox on the right
names_frame = Frame(window)
names_frame.pack(side=RIGHT, fill=Y)

# The three gender boxes on the righthand side
# Worth noting is that there is a slight gap between the bottommost entry
# in a gender listbox and the bottom of the box. While I could see that
# being visually irksome, I've tested it with the whole box filled out,
# and I think the slight gap actually helps with legibility. It doesn't
# look good when all three boxes have no gap between each other's entries.
new_neutral_names = Listbox(names_frame, bg='#8F6EB6', **options)
new_neutral_names.pack(fill=BOTH, expand=True)

new_male_names = Listbox(names_frame, bg='#7FC0F4', **options)
new_male_names.pack(fill=BOTH, expand=True)

new_female_names = Listbox(names_frame, bg='#F6B7CD', **options)
new_female_names.pack(fill=BOTH, expand=True)




# Favorites for names and generators
favorites_frame = Frame(window)
favorites_frame.pack(side=LEFT, fill=Y)

# Subframe for favoritegenerators
# This does not have a search bar, because if you have that many favorites that
# you need a search bar anyway, it completely defeats the purpose of the window
generators_frame = Frame(favorites_frame)
generators_frame.pack(fill=BOTH, expand=True)

favorite_generators_scroll = Scrollbar(generators_frame)
favorite_generators_scroll.pack(side=RIGHT, fill=Y)

favorite_generators = Listbox(generators_frame, bg="#FEB244", yscrollcommand=favorite_generators_scroll.set, **options)
favorite_generators.pack(fill=BOTH, expand=True)

favorite_generators_scroll.config(command=favorite_generators.yview)



# Imports user favorite generators. The main program saves them as a .txt file
def initializeFavoriteGenerators():
    with open('favorite_generators_storage.txt', 'r', encoding="utf-8") as f:
        user_generators = f.read()
        user_generators = user_generators.split("@")
    if not user_generators[-1]:
        user_generators.pop()
    user_generators.sort(reverse=True)
    return user_generators

def resetFavoriteGenerators():
    with open('favorite_generators_storage.txt', 'w', encoding="utf-8") as f:
        f.write("Bandit Names@Chinese Names@Demon Names@Dwarf Names@Edwardian Names@Elf Names@Hispanic Names@Moorish Names@Native American Names@Orc Names@")

# If favorites file doesn't exist, it will create a default one
try:
    user_generators = initializeFavoriteGenerators()
except:
    resetFavoriteGenerators()
    user_generators = initializeFavoriteGenerators()

# If favorites file is corrupted, it returns it to its default state
for i in user_generators:
    if i not in master_keys:
        resetFavoriteGenerators()

# With error handling out of the way, actually populates the user favorites list
user_generators = initializeFavoriteGenerators()
for i in user_generators:
    favorite_generators.insert(0, i)



# Subframe for favoritenames
favorite_names_frame = Frame(favorites_frame)
favorite_names_frame.pack(fill=BOTH, expand=True)

favorite_names_scroll = Scrollbar(favorite_names_frame)
favorite_names_scroll.pack(side=RIGHT, fill=Y)

favorite_names = Listbox(favorite_names_frame, bg="#ADD47F", yscrollcommand=favorite_names_scroll.set, **options)
favorite_names.pack(fill=BOTH, expand=True)

favorite_names_scroll.config(command=favorite_names.yview)

def getStoredNames():
    with open('favorite_names_storage.txt', 'r', encoding="utf-8") as f:
        user_names = f.read()
        user_names = user_names.split("@")
        #Ignore blank entries
        user_names = [x for x in user_names if x.strip()]
    return user_names

# Checks if stored name count exceeds 100, then gets rid of oldest entries
def cullStoredNames():
    user_names = getStoredNames()
    excess = len(user_names) - 100
    if excess > 0:
        print("test")
        with open('favorite_names_storage.txt', 'w', encoding="utf-8") as f:
            for i in range(100):
                f.write(user_names[excess+i] + "@")
        user_names = getStoredNames()
    return user_names

# Import user favorites unless missing. @ is used as a separator because some names contain commas.
try:
    user_names = cullStoredNames()
    if not user_names[-1]:
        user_names.pop()
    for i in (user_names):
        favorite_names.insert(200, i)
except:
    pass

# Scroll to the bottom, since that's the newest entry
favorite_names.yview_moveto(1.0)


# List of all generators
biglistframe = Frame(window)
biglistframe.pack(side=BOTTOM)

# Search bar
search_bar_text = Label(biglistframe, text="Search available generators", font=("Castellar", 16, "bold"), bg="#DADADA")
search_bar_text.pack(side=TOP, fill=X)
support_link = Label(biglistframe, text="(Even more available at https://www.fantasynamegenerators.com/)", font=('Helveticabold', 12), fg="blue", cursor="hand2", bg="#DADADA")
support_link.pack(side=TOP, fill=X)
search_bar = Entry(biglistframe, justify=CENTER, font=("", 16), bg="#E5DC84")
search_bar.pack(side=TOP, fill=X)

# This just opens the fantasy name generator's website and is bound above the search bar
def callback(url):
   webbrowser.open_new_tab(url)

# Uses whatever is in searchbar to curate the list of all generators
# Populate() is another function that actually adds the curated list at teh end
def search(event):
    x = search_bar.get()
    searched_list = []
    for i in master_keys:
        if x.lower() in i.lower():
            searched_list.append(i)
    populate(searched_list)

# Sadly implementing scrollbar (w) is a little messy, parts of it come before the list and one part has to be after the list is defined
tree_scroll = Scrollbar(biglistframe)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(biglistframe, yscrollcommand=tree_scroll.set, column=("c1", "c2", "c3"), show='headings', height=15)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="1")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="2")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="3")
tree.pack()

tree_scroll.config(command=tree.yview)




# This adds every key from master_dict (master_keys is its own list derived from master_dict) to the visible list
def populate(current_list):
    delete()
    remainder = len(current_list) % 3
    for i in range(0, len(current_list)-remainder, 3):
        tree.insert('', 'end', values=(current_list[i], current_list[i+1], current_list[i+2]))
    if remainder == 1:
        tree.insert('', 'end', values=(current_list[-1], "", ""))
    if remainder == 2:
        tree.insert('', 'end', values=(current_list[-2], current_list[-1], ""))

# Deletes all entries from the main list
def delete():
    tree.delete(*tree.get_children())

# Web_generate is DEPRECATED. I'm leaving it in just in case, but it's not used anymore.
# ...
# ...
# Generates names by going to the actual website and launching
# a chrome instance with Selenium
def web_generate(url):
    names = name_generator.generate_names(url)
    def x(key, output_box):
        output_box.delete(0, END)
        if names.get(key):
            for i in names[key]:
                output_box.insert(0, i)

    x("Male Names", new_male_names)
    x("Female Names", new_female_names)
    x("Neutral Names", new_neutral_names)

# Main name generator function, which draws from a list of 423
# converted Python scripts. The number of names the function outputs
# lines up precisely with what gender boxes it fills. They've all
# been specially tweaked to output consistent results. Single output
# generators always populate to neutral names, but otherwise the order
# is always as follows: the first 10 names are masculine, the next 10
# are feminine, and if there are more, the final 10 are neutral.
def internal_generate(index):
    func_name = f"python_gen{index}"
    names = getattr(converted_functions, func_name)()

    new_neutral_names.delete(0, END)
    new_male_names.delete(0, END)
    new_female_names.delete(0, END)

    def x(names_to_add, output_box):
        for i in names_to_add:
            output_box.insert(0, i)

    if len(names) == 10:
        x(names, new_neutral_names)
    elif len(names) == 20:
        x(names[0:10], new_male_names)
        x(names[10:20], new_female_names)
    elif len(names) == 30:
        x(names[0:10], new_male_names)
        x(names[10:20], new_female_names)
        x(names[20:30], new_neutral_names)
    else:
        print(f"Something went wrong. Total number of names = {len(names)}.")

# Calls the generate function when clicking on an item in the main list
# Known minor issue is that it highlights the entire row, not just the
# entry you clicked on; I've made peace with leaving that imperfection be
def entry_click(event):
    row = tree.identify_row(event.y)
    if row:
        column = int((tree.identify_column(event.x)).strip("#")) - 1
        values = tree.item(row, "values")
        # b.config (text = values[column])
        # c.config (text = master_dict[values[column]])
        # url = master_dict[values[column]]
        # web_generate(url)
        generator_index = master_keys.index(values[column])
        internal_generate(generator_index)
        play_sound("actionNoise")

# Calls the generate function when clicking on an item in the favorites list
def favorite_click(event):
    selected_index = favorite_generators.curselection()
    if selected_index:
        selected_item = favorite_generators.get(selected_index[0])
        # web_generate(master_dict[selected_item])
        internal_generate(master_keys.index(selected_item))
        play_sound("actionNoise")

# Adds a generator from the main list to favorites
def add_favorite_generator(event):
    row = tree.identify_row(event.y)
    if row:
        column = int((tree.identify_column(event.x)).strip("#")) - 1
        values = tree.item(row, "values")
        if values[column] not in favorite_generators.get(0, END):
            favorite_generators.insert(0, values[column])
            # This section alphabetizes the list
            sorted_list = []
            for i in favorite_generators.get(0, END):
                sorted_list.append(i)
            sorted_list.sort()
            favorite_generators.delete(0, END)
            for i in sorted_list:
                favorite_generators.insert(END, i)
            # Save the new favorite permanently
            with open('favorite_generators_storage.txt', 'a', encoding="utf-8") as f:
                f.write(values[column] + "@")
            play_sound("addNoise")

# Removes a generator from the favorites list
def remove_favorite_generator(event):
    favorite_generators.selection_set(favorite_generators.nearest(event.y))
    selected_index = favorite_generators.curselection()
    if selected_index:
        selected_item = selected_index[0]
        favorite_generators.delete(selected_item)
        # Remove the favorite from the persistent user favorites file
        sorted_list = []
        for i in favorite_generators.get(0, END):
            sorted_list.append(i)
        with open('favorite_generators_storage.txt', 'w', encoding="utf-8") as f2:
            for i in sorted_list:
                f2.write(i + "@")
        play_sound("removeNoise")

# Saves a recently generated name to a recent favorites list, which contains 100 entries
# This is intended as more of a running log of recently chosen names; in reality, if a
# user finds a name they like and want to use long-term, they're bound to write it down
# in whatever they're using it for, be it DnD or a novel. That's why there is somewhat
# limited functionality here. It would be kind of weird to just save thousands of
# previously used names forever and have to remove them manually here.
def add_favorite_name(event):
    listbox = event.widget  # The Listbox that triggered the event
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index[0])
        # Deletes the oldest entry and caps the list at 100. Even if through a bug someone
        # adds many more than 100 entries, it will get rid of all the excess until it has exactly 100.
        # This logic may seem redundant instead of just calling cullStoredNames, but that would involve
        # rewriting the whole file every single time. This is honestly good enough and yields better
        # performance 99.9% of the time, at the cost of one user who adds a billion names in one session
        # and crashes their next one.
        if favorite_names.size() >= 100:
            overflow = favorite_names.size() - 100
            favorite_names.delete(0, overflow)
        favorite_names.insert(END, selected_item)
        # Save it to the persistent user favorite names for use between sessions
        with open('favorite_names_storage.txt', 'a', encoding="utf-8") as f:
            f.write(selected_item+"@")
        play_sound("addNoise")
        # Scroll to the bottom, since that's the newest entry
        favorite_names.yview_moveto(1.0)



# Binding functions to certain UI elements
# Most of these are here instead of with the things they're bound to
# So that they come after the relevant functions
tree.bind('<Button-1>', entry_click)
tree.bind('<Button-3>', add_favorite_generator)
for child in names_frame.winfo_children():
    if isinstance(child, Listbox):
        child.bind('<<ListboxSelect>>', add_favorite_name)
favorite_generators.bind('<<ListboxSelect>>', favorite_click)
favorite_generators.bind('<Button-3>', remove_favorite_generator)
search_bar.bind('<KeyRelease>', search)
canvas.tag_bind(rect, "<Button-1>", lambda e: mute_toggle(mute))
support_link.bind("<Button-1>", lambda e: callback("https://www.fantasynamegenerators.com/"))



# Initialization - populates the UI list with the full internal generator list,
# Plus loops the main window
populate(master_keys)
window.mainloop()