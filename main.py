import copy
import random
from tkinter import *
from PIL import Image, ImageTk
from TopicModeling.model_api import *
from Sketchformer.sketchformer_api import *

root = Tk()
root.title('Sketch Game: Why is this object here?')
root.geometry("1000x1000")
root.attributes('-fullscreen', True)


width = 1000
height = 800
obj_limit = 4
round_counter = 0
pred_multi_cnt = 3
multi_conf_thold = 0.1

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
context_list = ["bakery", "sea", "bathroom", "school", "airport", "river", "cafe", "farm", "factory", "hospital"]
curr_context = None
model = get_model()

def close_app(*args):
    root.destroy()

def get_drawing(event):
    global stroke_drawing
    global old_coords
    global stroke
    global my_canvas, memory_canvas_arr, color_list
    global round_counter

    x_cor, y_cor = event.x, event.y

    if old_coords:
        x1 = old_coords[0]
        y1 = old_coords[1]

        if round_counter < 2:
            line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill="black", width=3)
        else:
            if (len(memory_canvas_arr) > 0):
                for i in range(0, len(memory_canvas_arr)):
                    for s in memory_canvas_arr[i]:
                        my_canvas.itemconfig(s, fill=color_list[i % len(color_list)])

            line = my_canvas.create_line(x1, y1, x_cor, y_cor, fill=color_list[round_counter], width=3)

        stroke_drawing.append(line)
    old_coords = [x_cor, y_cor]
    stroke.append([x_cor, y_cor, 0])

def simplification():
    global image, simplified_sketch

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
    memory_canvas_arr.append(stroke_drawing)

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
    memory_canvas_arr = []
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
        Result = "\nWARNING!! Please draw 6 sketch objects in total. \n Keep going...\n\n\n"
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
            for object_list in object_lists:
                # remove duplicates
                set_obj = set(object_list)
                if len(object_list) > len(set_obj):
                    continue

                hidden_obj, topic_prob, max_topic_idx, max_img = find_unrelated(object_list, curr_context)
                print(object_list, "-->", hidden_obj, "-", topic_prob)
                if max_topic_prob < topic_prob:
                    max_topic_prob = topic_prob
                    max_set_obj = copy.deepcopy(object_list)
                    max_hidden_obj = hidden_obj
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

            found_image_path = 'topic_images/' + str(max_topic_idx) + "/" + max_img
            print("found_image_path ", found_image_path)
            found_image = Image.open(found_image_path)
            my_canvas.create_image(0, 0, image=ImageTk.PhotoImage(found_image), anchor="nw")
            my_canvas.bind("<Configure>")

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
        dummy = memory_canvas_arr.pop()
        for s in last_stroke:
            my_canvas.delete(s)

        image.pop()
        old_coords = None

def keep_next_object():
    global simplified_sketch
    global image, my_canvas
    global canvas_arr, res
    global turn_label
    global turn_text, memory_canvas_arr
    global obj_limit, round_counter

    simplification()

    if round_counter < 2:
        if (len(canvas_arr) > 0):
            for i in range(0, len(canvas_arr)):
                for s in canvas_arr[i]:
                    my_canvas.itemconfig(s, fill='white')

    round_counter += 1
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