import os
from tkinter import *
from PIL import Image, ImageTk

from Sketchformer.sketchformer_api import *

root = Tk()
root.title('Sketch Game: Why is this object here?')
root.geometry("1000x1000")

width = 1000
height = 800

# Global variables
drawing = False
image = []
stroke = []
counter = 1
simplified_sketch = []
canvas_arr = []
old_coords = None
pen_drawing = []
stroke_drawing = []
next_object_button = None
done_button = None
clear_button = None
undo_button = None
start_btn = None
yes_button= None
no_button = None
l = None
t = None
my_img = None
img = None
bg = None
res = None
my_canvas = None

model = get_model()

def get_drawing(event):
    # pencil drawing.
    global pen_drawing
    global stroke_drawing
    global old_coords
    global stroke
    global my_canvas

    x_cor, y_cor = event.x, event.y

    if old_coords:
        x1 = old_coords[0]
        y1 = old_coords[1]

        line = my_canvas.create_line(x1, y1, x_cor, y_cor, width=3)
        pen_drawing.append(line)
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
    global canvas_arr
    global stroke_drawing

    stroke[-1][-1] = 1
    image.extend(stroke)
    stroke = []
    old_coords = None

    canvas_arr.append(stroke_drawing)
    stroke_drawing = []

def clear_canvas():
    global my_canvas
    global canvas_arr
    global image
    global old_coords
    global simplified_sketch

    canvas_arr = []
    image = []
    old_coords = None
    simplified_sketch = []
    my_canvas.delete("all")

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
    my_canvas.itemconfig(my_img, image =photo1 )
    width = new_width
    height = new_height

def result_screen():
    global image
    global done_button
    global next_object_button
    global clear_button
    global yes_button
    global no_button
    global res

    if len(image) > 0:
        keep_next_object()
    object_list = predict(model, simplified_sketch)

    # TODO: Add classification and other processing pipelines

    hidden_obj = object_list[-1]  # TODO: Topic modeling will find the hidden object.

    Result = """
WE FOUND IT !!!
Your hidden object is: """
    Result += hidden_obj + "\n\nYou sketch the followings in order: \n"

    for i in range(len(object_list)):
        Result += object_list[i] + "\n"

    Result += "\nCould I find the hidden object correctly?              \n"
    res = Label(root, text=Result)
    res.config(font=("Courier", 14), bg="#B86CB5")

    res.place(relx=0.5, rely=0.5, anchor="center")

    if (done_button is not None): done_button.destroy()
    if (next_object_button is not None): next_object_button.destroy()
    if (clear_button is not None): clear_button.destroy()
    if (undo_button is not None): undo_button.destroy()

    yes_button = Button(res, text="YES", font=("Courier", 9), width=7, fg="#336d92", command=welcome_screen)
    yes_button.place(relx=0.81, rely=0.89, anchor='center')
    no_button = Button(res, text="NO", font=("Courier", 9), width=7, fg="#336d92", command=welcome_screen)
    no_button.place(relx=0.93, rely=0.89, anchor='center')

def last_canvas():
    global canvas_arr
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
    global image
    global canvas_arr

    simplification()
    image = []
    canvas_arr = []

def drawing_screen():
    global my_img
    global done_button
    global next_object_button
    global clear_button
    global undo_button
    global start_btn
    global t
    global l
    global my_canvas

    next_object_button = Button(root, text="NEXT OBJECT", font=("Courier", 10), width=10, fg="#336d92",
                                command=keep_next_object)
    done_button = Button(root, text="DONE", font=("Courier", 10), width=10, fg="#336d92", command=result_screen)
    clear_button = Button(root, text="DELETE", font=("Courier", 10), width=10, fg="#336d92", command=clear_canvas)
    undo_button = Button(root, text="UNDO", font=("Courier", 10), width=10, fg="#336d92", command=last_canvas)

    if (start_btn is not None):  start_btn.destroy()
    if (l is not None):  l.destroy()
    if (t is not None):  t.destroy()

    my_canvas.delete(my_img)

    next_object_button.place(relx=0.92, rely=0.09, anchor='s')
    done_button.place(relx=0.92, rely=0.20, anchor='s')
    clear_button.place(relx=0.92, rely=0.30, anchor='s')
    undo_button.place(relx=0.92, rely=0.40, anchor='s')
    # Use left mouse button to draw.
    my_canvas.bind("<B1-Motion>", get_drawing)
    my_canvas.bind("<ButtonRelease-1>", end_stroke)

    root.bind("<Delete>", clear_canvas)

def welcome_screen():
    global my_img
    global l
    global t
    global start_btn
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
    Fact = """
Please draw your desired scene 
to the canvas. Add one additional 
sketch object which normally 
does not belong to that scene. 

Then, we will find the object
you hide from us :) 

NOTE: CLICK to NEXT OBJECT button 
after drawing each individual object
to the scene. CLICK DONE when you 
finish your sketch. \n\n
"""
    l = Label(root, text="INSTRUCTIONS")
    l.config(font=("Courier", 14), bg= "#B86CB5")

    t = Label(root, text=Fact)
    t.config(font=("Courier", 14), bg= "pink")

    start_btn = Button(t, text="START", font=("Courier", 14), width=15, fg="#121111", bg= "#E4E4E0", command=drawing_screen)

    l.place(relx=0.5, rely=0.32, anchor="center")
    t.place(relx=0.5, rely=0.55, anchor="center")
    start_btn.place(relx=0.5, rely=0.92, anchor="center")

welcome_screen()
root.mainloop()