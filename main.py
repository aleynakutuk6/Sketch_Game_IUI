import copy
import random
from tkinter import *
from PIL import Image, ImageTk
from TopicModeling.model_api import *
from Sketchformer.sketchformer_api import *

import cv2

root = Tk()
root.title('Sketch Game: Why is this object here?')
root.geometry("1000x1000")
root.attributes('-fullscreen', True)


width = 1000
height = 800
obj_limit = 2
round_counter = 0
pred_multi_cnt = 3
multi_conf_thold = 0.15

# Global variables
drawing = False
image = []
stroke = []
counter = 1
simplified_sketch = []
canvas_arr = []
memory_canvas_arr = []
old_coords = None
stroke_drawing = []
next_object_button = None
done_button = None
warning_exit_btn = None
separator_line = None
clear_button = None
undo_button = None
next_btn = None
yes_button= None
no_button = None
mylist = None
scrollbar = None
l = None
turn_label = None
context_label = None
list_classes = None
t = None
my_img = None
img = None
bg = None
res = None
my_canvas = None
player_1 = None
player_2 = None
label_players = None
start_button = None
turn_text = None
player1_name = StringVar()
player2_name = StringVar()
color_list = ["green", "pink", "blue", "red", "purple", "orange", "brown", "black"]
context_list = ["bakery", "sea", "bathroom", "school", "airport", "river", "cafe", "farm", "sports", "hospital"]
curr_context = None

temp_arr = [[],[]]
model = get_model()

def close_app(*args):
    root.destroy()

def get_drawing(event):
    global stroke_drawing
    global old_coords, temp_arr
    global stroke, turn_text
    global my_canvas, memory_canvas_arr, color_list
    global round_counter

    x_cor, y_cor = event.x, event.y

    if old_coords:
        x1 = old_coords[0]
        y1 = old_coords[1]

        if turn_text == player1_name.get():
            if len(memory_canvas_arr) > 1:
                for s in memory_canvas_arr[-2]:
                    for l in s:
                        my_canvas.itemconfig(l, fill="black")
        elif turn_text == player2_name.get():
            if len(memory_canvas_arr) > 0:
                for s in memory_canvas_arr[-1]:
                    for l in s:
                        my_canvas.itemconfig(l, fill="white")
        """
        if round_counter < 2:
            line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill="black", width=3)
        elif round_counter == 2:
            if (len(memory_canvas_arr) > 0):
                for i in range(0, len(memory_canvas_arr)):
                    for s in memory_canvas_arr[i]:
                        my_canvas.itemconfig(s, fill=color_list[i % len(color_list)])
            line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill="black", width=3)
        else:
            line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill=color_list[round_counter], width=3)
        """
        line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill="black", width=3)
        stroke_drawing.append(line)

    old_coords = [x_cor, y_cor]
    temp_arr[0].append(old_coords[0])
    temp_arr[1].append(old_coords[1])
    stroke.append([x_cor, y_cor, 0])

def simplification():
    global image, simplified_sketch

    image = [[284, 205, 0], [282, 203, 0], [281, 202, 0], [279, 201, 0], [277, 198, 0], [276, 197, 0], [274, 195, 0], [273, 194, 0], [271, 193, 0], [270, 191, 0], [269, 190, 0], [267, 188, 0], [266, 187, 0], [264, 186, 0], [263, 185, 0], [262, 184, 0], [259, 184, 0], [258, 183, 0], [257, 183, 0], [255, 183, 0], [252, 184, 0], [250, 185, 0], [248, 186, 0], [245, 187, 0], [243, 188, 0], [241, 189, 0], [240, 191, 0], [238, 191, 0], [237, 193, 0], [236, 194, 0], [234, 196, 0], [233, 197, 0], [232, 198, 0], [232, 200, 0], [232, 201, 0], [232, 202, 0], [232, 204, 0], [232, 205, 0], [232, 206, 0], [232, 207, 0], [233, 209, 0], [235, 211, 0], [235, 212, 0], [237, 213, 0], [239, 215, 0], [241, 216, 0], [243, 217, 0], [245, 219, 0], [247, 219, 0], [248, 219, 0], [250, 220, 0], [250, 221, 0], [247, 223, 0], [245, 224, 0], [242, 226, 0], [237, 228, 0], [235, 229, 0], [232, 231, 0], [231, 232, 0], [229, 234, 0], [228, 235, 0], [227, 236, 0], [226, 238, 0], [226, 239, 0], [226, 241, 0], [226, 242, 0], [226, 245, 0], [226, 246, 0], [226, 249, 0], [228, 250, 0], [229, 253, 0], [230, 255, 0], [232, 256, 0], [233, 258, 0], [234, 259, 0], [236, 261, 0], [238, 262, 0], [239, 263, 0], [241, 264, 0], [243, 265, 0], [244, 266, 0], [247, 266, 0], [249, 266, 0], [250, 266, 0], [251, 266, 0], [253, 266, 0], [254, 266, 0], [255, 266, 0], [256, 265, 0], [256, 264, 0], [257, 264, 0], [256, 266, 0], [254, 269, 0], [252, 272, 0], [251, 275, 0], [250, 280, 0], [250, 283, 0], [250, 285, 0], [251, 287, 0], [253, 290, 0], [254, 291, 0], [256, 294, 0], [257, 295, 0], [260, 297, 0], [262, 298, 0], [265, 300, 0], [270, 302, 0], [275, 302, 0], [282, 303, 0], [289, 303, 0], [296, 302, 0], [301, 302, 0], [308, 300, 0], [314, 298, 0], [320, 296, 0], [323, 294, 0], [325, 293, 0], [326, 290, 0], [328, 289, 0], [328, 288, 0], [329, 286, 0], [329, 285, 0], [329, 284, 0], [329, 282, 0], [330, 284, 0], [331, 285, 0], [332, 287, 0], [334, 290, 0], [336, 291, 0], [338, 292, 0], [341, 294, 0], [344, 296, 0], [346, 296, 0], [349, 296, 0], [351, 296, 0], [354, 296, 0], [359, 294, 0], [362, 292, 0], [367, 290, 0], [370, 289, 0], [372, 287, 0], [375, 285, 0], [376, 282, 0], [378, 279, 0], [379, 275, 0], [380, 273, 0], [380, 269, 0], [380, 265, 0], [379, 262, 0], [379, 260, 0], [378, 259, 0], [378, 258, 0], [379, 258, 0], [381, 258, 0], [384, 258, 0], [387, 257, 0], [390, 255, 0], [395, 253, 0], [398, 252, 0], [400, 250, 0], [402, 249, 0], [404, 247, 0], [405, 246, 0], [407, 244, 0], [407, 241, 0], [408, 237, 0], [408, 234, 0], [408, 229, 0], [408, 226, 0], [407, 223, 0], [405, 219, 0], [403, 215, 0], [401, 213, 0], [399, 211, 0], [396, 209, 0], [394, 208, 0], [392, 206, 0], [390, 205, 0], [387, 204, 0], [386, 203, 0], [385, 203, 0], [384, 203, 0], [384, 201, 0], [383, 199, 0], [382, 197, 0], [381, 196, 0], [380, 194, 0], [379, 192, 0], [377, 190, 0], [376, 188, 0], [374, 187, 0], [373, 186, 0], [371, 184, 0], [369, 183, 0], [367, 182, 0], [364, 180, 0], [361, 180, 0], [358, 180, 0], [355, 180, 0], [351, 180, 0], [349, 180, 0], [347, 181, 0], [346, 182, 0], [344, 183, 0], [343, 185, 0], [341, 186, 0], [341, 187, 0], [340, 189, 0], [339, 189, 0], [338, 188, 0], [337, 186, 0], [335, 184, 0], [333, 181, 0], [332, 179, 0], [330, 177, 0], [329, 174, 0], [327, 173, 0], [326, 172, 0], [324, 170, 0], [323, 170, 0], [321, 168, 0], [320, 167, 0], [319, 167, 0], [317, 167, 0], [315, 167, 0], [311, 168, 0], [309, 170, 0], [307, 171, 0], [305, 173, 0], [303, 174, 0], [300, 176, 0], [299, 177, 0], [297, 179, 0], [296, 180, 0], [295, 181, 0], [293, 182, 0], [293, 183, 0], [291, 184, 0], [291, 185, 0], [290, 187, 0], [289, 189, 0], [289, 190, 0], [289, 191, 0], [288, 193, 0], [287, 193, 0], [287, 194, 0], [287, 195, 0], [287, 196, 0], [286, 196, 0], [286, 197, 0], [286, 198, 0], [286, 199, 0], [286, 200, 0], [287, 200, 0], [287, 201, 0], [287, 202, 0], [288, 202, 1]]

    image = apply_RDP(image)
    image = normalize(image)
    simplified_sketch.append(image)

    return simplified_sketch

def end_stroke(event):
    global old_coords
    global stroke
    global image
    global canvas_arr, memory_canvas_arr
    global stroke_drawing

    stroke[-1][-1] = 1
    image.extend(stroke)
    stroke = []
    old_coords = None

    canvas_arr.append(stroke_drawing)
    # memory_canvas_arr.append(stroke_drawing)

    stroke_drawing = []

def clear_canvas():
    global my_canvas
    global canvas_arr, memory_canvas_arr
    global image, separator_line
    global old_coords
    global turn_text
    global simplified_sketch
    global my_canvas
    global image
    global old_coords

    if (len(canvas_arr) > 0):
        for i in range(0, len(canvas_arr)):
            for s in canvas_arr[i]:
                my_canvas.delete(s)

    canvas_arr = []
    image = []
    old_coords = None

    separator_line = my_canvas.create_line(700, 20, 700, 850, fill="black", width=5)

def resize_image(event):
    global width
    global height
    global img
    global my_canvas

    new_width = event.width
    new_height = event.height

    img3 = img.resize((new_width, new_height), Image.ANTIALIAS)
    photo1 = ImageTk.PhotoImage(img3)
    my_canvas.image = photo1
    my_canvas.itemconfig(my_img, image=photo1)
    width = new_width
    height = new_height

def destroy_warning():
    global res, warning_exit_btn

    res.destroy()
    warning_exit_btn.destroy()

def result_screen():
    global image, separator_line
    global done_button, next_object_button, clear_button, mylist, scrollbar, yes_button, no_button
    global res, warning_exit_btn
    global player1_name, player2_name
    global turn_label, list_classes
    global pred_multi_cnt, multi_conf_thold
    global curr_context

    if len(simplified_sketch) != obj_limit:
        Result = f"\nWARNING!! Please draw {obj_limit} sketch objects in total. \n Keep going...\n\n\n"
        res = Label(root, text=Result)
        res.config(font=("Courier", 13), bg="pink", height=6, padx=15, pady=10)
        res.place(relx=0.5, rely=0.5, anchor="center")
        warning_exit_btn = Button(root, text="X", font=("Courier", 7), width=2, fg="white", bg="red", command=destroy_warning)
        warning_exit_btn.place(relx=0.662, rely=0.431, anchor="center")

    else:
        if (done_button is not None): done_button.destroy()
        if (next_object_button is not None): next_object_button.destroy()
        if (clear_button is not None): clear_button.destroy()
        if (undo_button is not None): undo_button.destroy()
        if (turn_label is not None): turn_label.destroy()
        if (mylist is not None): mylist.destroy()
        if (scrollbar is not None): scrollbar.destroy()
        if (list_classes is not None): list_classes.destroy()

        my_canvas.delete(separator_line)

        if len(simplified_sketch) != 0:

            if len(image) > 0:
                keep_next_object()

            if pred_multi_cnt == 1:
                object_lists = predict(model, simplified_sketch)
                object_lists = [object_lists]
            elif pred_multi_cnt > 1:
                object_lists = multi_predict(model, simplified_sketch, k=pred_multi_cnt, conf_thold=multi_conf_thold)
                object_lists = list(itertools.product(*object_lists))
            else:
                raise ValueError("Wrong multi-class value is entered: " + str(pred_multi_cnt))

            print("object_list ", object_lists)

            max_topic_prob = -1
            max_set_obj = None
            max_hidden_obj = None
            max_found_img, max_found_doc = None, None
            for object_list in object_lists:
                # remove duplicates
                set_obj = set(object_list)
                if len(object_list) > len(set_obj):
                    continue

                hidden_obj, topic_prob, max_topic_idx, max_img, max_doc = find_unrelated(object_list, curr_context)
                print(object_list, "-->", hidden_obj, "-", topic_prob)
                if max_topic_prob < topic_prob:
                    max_topic_prob = topic_prob
                    max_set_obj = copy.deepcopy(object_list)
                    max_hidden_obj = hidden_obj
                    max_found_img = max_img
                    max_found_doc = max_doc
                    for id, h in enumerate(object_list):
                        if h == hidden_obj:
                            hidden_idx = id
                            break

            Result = f"""
WE FOUND IT !!!
The most unrelated object is: {max_hidden_obj}

--> {player1_name.get() if hidden_idx % 2 == 0 else player2_name.get()} LOSES :(

You sketch the followings in order:

"""
            for i in range(len(max_set_obj)):
                Result += max_set_obj[i] + "\n"

            Result += "\nCould I find the hidden object correctly?              \n"
            res = Label(root, text=Result)
            res.config(font=("Courier", 14), bg="pink")
            res.place(relx=0.5, rely=0.5, anchor="center")

            yes_button = Button(res, text="YES", font=("Courier", 9), width=7, fg="#336d92", command=welcome_screen)
            yes_button.place(relx=0.81, rely=0.89, anchor='center')
            no_button = Button(res, text="NO", font=("Courier", 9), width=7, fg="#336d92", command=welcome_screen)
            no_button.place(relx=0.93, rely=0.89, anchor='center')

            found_image_path = 'topic_images/' + max_found_img
            print("found_image_path ", found_image_path)
            print("found_doc ", max_found_doc)

            cv2.imshow("Most Similar Image", cv2.imread(found_image_path))
            """
            found_image = Image.open(found_image_path)
            my_canvas.create_image(0, 0, image=ImageTk.PhotoImage(found_image), anchor="nw")
            my_canvas.bind("<Configure>")
            """

        else:
            Result = "\nERROR!! You did not draw anything... Why? :((((\n\n\n"
            res = Label(root, text=Result)
            res.config(font=("Courier", 14), bg="pink", padx=15, pady=8)
            res.place(relx=0.5, rely=0.5, anchor="center")

            yes_button = Button(res, text="MAIN PAGE", font=("Courier", 14), width=10, fg="#121111", command=welcome_screen)
            yes_button.place(relx=0.5, rely=0.7, anchor='center')

def last_canvas():
    global canvas_arr, memory_canvas_arr
    global my_canvas
    global image
    global old_coords

    if(len(canvas_arr) > 0):
        last_stroke = canvas_arr.pop()
        for s in last_stroke:
            my_canvas.delete(s)

        image.pop()
        old_coords = None

def keep_next_object():
    global simplified_sketch
    global image, my_canvas
    global canvas_arr, res, memory_canvas_arr
    global turn_label
    global turn_text
    global obj_limit, round_counter

    simplification()
    """
    if round_counter < 2:
        if (len(canvas_arr) > 0):
            for i in range(0, len(canvas_arr)):
                for s in canvas_arr[i]:
                    my_canvas.itemconfig(s, fill='white')
    """

    memory_canvas_arr.append(canvas_arr)
    # round_counter += 1
    image = []
    canvas_arr = []

    if turn_text == player1_name.get():
        turn_text = player2_name.get()
        bg = "pink"
        turn_label.config(text="Your Turn: " + turn_text, bg=bg)
        turn_label.place(relx=0.60, rely=0.04, anchor="nw")
    elif turn_text == player2_name.get():
        turn_text = player1_name.get()
        bg = "#B86CB5"
        turn_label.config(text="Your Turn: " + turn_text, bg=bg)
        turn_label.place(relx=0.15, rely=0.04, anchor="nw")

    if turn_text == player1_name.get():
        if len(memory_canvas_arr) > 1:
            for s in memory_canvas_arr[-2]:
                for l in s:
                    my_canvas.itemconfig(l, fill="black")
    elif turn_text == player2_name.get():
        if len(memory_canvas_arr) > 0:
            for s in memory_canvas_arr[-1]:
                for l in s:
                    my_canvas.itemconfig(l, fill="white")

    if len(simplified_sketch) == obj_limit:
        result_screen()

def players_screen():
    global next_btn
    global t
    global l
    global player_1
    global player_2
    global label_players
    global player1_name
    global player2_name
    global start_button


    if (next_btn is not None):  next_btn.destroy()
    if (l is not None):  l.destroy()
    if (t is not None):  t.destroy()
    my_canvas.delete(my_img)

    players_txt = """
Please enter players' names below: \n\n\n\n\n\n\n\n
    """
    label_players = Label(root, text=players_txt)
    label_players.config(font=("Courier", 14), bg="pink", padx=24, pady=16)
    label_players.place(relx=0.5, rely=0.5, anchor="center")

    player1_name = StringVar()
    player2_name = StringVar()

    player_1 = Entry(label_players, textvariable=player1_name, font=("Courier", 20), bd=0, width=10, bg="white")
    player_1.insert(0, 'Player 1')
    player_1.place(relx=0.5, rely=0.45, anchor="center")

    player_2 = Entry(label_players, textvariable=player2_name, font=("Courier", 20), bd=0, width=10, bg="white")
    player_2.insert(0, 'Player 2')
    player_2.place(relx=0.5, rely=0.63, anchor="center")

    start_button = Button(label_players, text="START", font=("Courier", 14), width=15,  fg="#121111",
                                command=drawing_screen)
    start_button.place(relx=0.5, rely=0.90, anchor='s')

def drawing_screen():
    global my_img
    global done_button, next_object_button, scrollbar, mylist, clear_button, undo_button, next_btn, start_button
    global t, l
    global turn_label, list_classes, turn_text
    global my_canvas
    global player_1, player_2, label_players, player1_name, player2_name
    global separator_line
    global context_list, context_label, curr_context

    next_object_button = Button(root, text="NEXT OBJECT", font=("Courier", 9), width=15, fg="#121111", command=keep_next_object)
    done_button = Button(root, text="DONE", font=("Courier", 9), width=15, fg="#121111", command=result_screen)
    clear_button = Button(root, text="DELETE", font=("Courier", 9), width=15, fg="#121111", command=clear_canvas)
    undo_button = Button(root, text="UNDO", font=("Courier", 9), width=15, fg="#121111", command=last_canvas)

    with open("C:/Users/aleyn/OneDrive/Masaüstü/COMP537-IUI/IUI_Project_SketchGame/Sketch_Game_IUI/Sketchformer/prep_data/quickdraw/list_quickdraw.txt") as file:
        quickdraw_classes = file.readlines()

    scrollbar = Scrollbar(root, orient=HORIZONTAL)
    mylist = Listbox(root, yscrollcommand=scrollbar.set, font=("Courier", 10), width=24)
    for c in quickdraw_classes:
        mylist.insert(END, str(c))

    scrollbar.config(command=mylist.yview)

    turn_text = player1_name.get()
    turn_label = Label(root, text="Your Turn: " + turn_text)
    turn_label.config(font=("Courier", 13), bg="#B86CB5")

    curr_context = random.choice(context_list)
    context_label = Label(root, text="Context: " + curr_context)
    context_label.config(font=("Courier", 15), bg="#E4E4E0")

    separator_line =my_canvas.create_line(700, 60, 700, 800, fill="black", width=5)

    list_classes = Label(root, text="List of available \n objects")
    list_classes.config(font=("Courier", 12), bg="white")

    if (start_button is not None):  start_button.destroy()
    if (player_1 is not None):  player_1.destroy()
    if (player_2 is not None):  player_2.destroy()
    if (label_players is not None):  label_players.destroy()

    #my_canvas.delete(my_img)

    context_label.place(relx=0.515, rely=0.03, anchor='ne')
    next_object_button.place(relx=0.95, rely=0.06, anchor='ne')
    done_button.place(relx=0.95, rely=0.10, anchor='ne')
    clear_button.place(relx=0.95, rely=0.14, anchor='ne')
    undo_button.place(relx=0.95, rely=0.18, anchor='ne')
    list_classes.place(relx=0.98, rely=0.23, anchor='ne')
    mylist.place(relx=0.98, rely=0.28, anchor='ne')
    scrollbar.place(relx=0.98, rely=0.28, anchor='ne')

    turn_label.place(relx=0.15, rely=0.04, anchor="nw")

    # Use left mouse button to draw.
    my_canvas.bind("<B1-Motion>", get_drawing)
    my_canvas.bind("<ButtonRelease-1>", end_stroke)

    root.bind("<Delete>", clear_canvas)

def welcome_screen():
    global my_img
    global l,t
    global next_btn
    global yes_button
    global no_button
    global bg
    global img
    global my_canvas

    if(my_canvas is not None):
        clear_canvas()
        my_canvas.destroy()
    if (yes_button is not None):  yes_button.destroy()
    if (no_button is not None):  no_button.destroy()
    if (res is not None):  res.destroy()

    # Define Canvas
    my_canvas = Canvas(root, width=width, height=height, bd=0, highlightthickness=0, bg="white")
    my_canvas.pack(fill="both", expand=True)

    # Define Background Image
    background_image = Image.open('Images/background.jpg')
    img = background_image.resize((width, height))
    bg = ImageTk.PhotoImage(img)

    # Put the image on the canvas
    my_img = my_canvas.create_image(0, 0, image=bg, anchor="nw")
    my_canvas.bind("<Configure>", resize_image)  # load image only when commenting this out
    Fact = f"""
In the next page, you will be given with a canvas.
At each turn, one player will draw a sketch object
and the other will wait. 

At the end, we will find the most unrelated sketch object and 
whoever draws it, LOSES THE GAME!!

NOTE: CLICK to NEXT OBJECT button after drawing 
each individual object to the scene.

WARNING! Game will end when each player 
sketches {obj_limit//2} object instances. \n\n
"""
    l = Label(root, text="INSTRUCTIONS")
    l.config(font=("Courier", 14), bg= "#B86CB5")

    t = Label(root, text=Fact)
    t.config(font=("Courier", 14), bg= "pink", padx=20)

    exit_btn = Button(
        root, text="X", font=("Courier", 12), width=2,
        fg="white", bg="red", command=root.destroy)

    exit_btn.place(relx=0.99, rely=0.01, anchor="ne")

    next_btn = Button(t, text="NEXT", font=("Courier", 14), width=15, fg="#121111", bg= "#E4E4E0", command=players_screen)

    l.place(relx=0.5, rely=0.32, anchor="center")
    t.place(relx=0.5, rely=0.55, anchor="center")
    next_btn.place(relx=0.5, rely=0.92, anchor="center")

welcome_screen()
root.bind("<Escape>", close_app)
root.mainloop()