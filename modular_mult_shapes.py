# Modular multiplication shapes
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk # used for combobox which does not exist in tk
from PIL import Image, ImageDraw, ImageFont # used for saving image files
from math import *

# calculate coordinates of points on shape and store in lists
def calc_coords(shape): 
    new_x_list = []; new_y_list = []
    if shape == "circle":
        for n in range(m.get()):
            angle = 2.0 * pi * n / m.get()  + pi / 2.0
            new_x_list.append( x_center - int(radius * cos(angle)) )
            new_y_list.append( y_center - int(radius * sin(angle)) )
    elif shape == "triangle":
        # calculate coordinates of points on triangle and store in lists
        side = int(m.get() / 3) 
        for n in range(side):
            new_x_list.append( x_center + int(- radius + radius * n / side))
            new_y_list.append( y_center + int(alpha * (+ radius  - 2 * radius * n / side)))
        for n in range(side):
            new_x_list.append( x_center + int(radius * n / side ))
            new_y_list.append( y_center + int(alpha * (- radius + 2 * radius * n / side)))
        for n in range(side):
            new_x_list.append( x_center + int(radius  - 2 * radius * n / side))
            new_y_list.append( y_center + int(alpha * radius) )
    elif shape == "square":
        # calculate coordinates of points on square and store in lists
        side = int(m.get() / 4) 
        for n in range(side):
            new_x_list.append( x_center - radius  + int(2 * radius * n / side) )
            new_y_list.append( y_center - radius )
        for n in range(side):
            new_x_list.append( x_center + radius )
            new_y_list.append( y_center - radius  + int(2 * radius * n / side))
        for n in range(side):
            new_x_list.append( x_center + radius  - int(2 * radius * n / side) )
            new_y_list.append( y_center + radius )
        for n in range(side):
            new_x_list.append( x_center - radius )
            new_y_list.append( y_center + radius  - int(2 * radius * n / side) )           
    return new_x_list, new_y_list

# draw the outline of the circle, triangle or square
def draw_outline(shape):
    # determine outline color
    if combo_color.get() == "color":
        line_color = "white"
    else:
        line_color = combo_color.get()
    # clear image PIL
    draw.rectangle([(0,0),(screen_width,screen_height)],fill = "black", outline = None)
    if shape == "circle":
        # draw circle on tkinter canvas
        canvas1.create_oval(x_center - radius, y_center - radius,
                            x_center + radius, y_center + radius,
                            outline = line_color, fill = "")
        # draw circle on PIL image
        draw.ellipse([(x_center - radius, y_center - radius),
                      (x_center + radius, y_center + radius)],
                     fill = None, outline = "white")
    elif shape == "triangle":
        # draw triangle
        x_triangle = [x_center - radius,
                      x_center,
                      x_center + radius]
        y_triangle = [y_center + int(alpha * radius),
                      y_center - int(alpha * radius),
                      y_center + int(alpha * radius)]
        # add triangle to tkinter canvas
        canvas1.create_polygon(list(zip(x_triangle,y_triangle)), outline = line_color)
        # add triangle to PIL image
        draw.polygon(list(zip(x_triangle,y_triangle)), outline = line_color)
    elif shape == "square":
        # draw square on tkinter canvas
        canvas1.create_rectangle(x_center - radius, y_center - radius,
                            x_center + radius, y_center + radius,
                            outline = line_color, fill = "")
        # draw square on PIL image
        draw.rectangle([(x_center - radius, y_center - radius),
                      (x_center + radius, y_center + radius)],
                     fill = None, outline = "white")

# this function draws a actual image
# output is done both on the tkinter canvas for real time viewing
# and on a PIL image to be able to export to a PNG image file later
def draw_image(slider_value):
    x_list, y_list = calc_coords(combo_shape.get())
    # clear screen tkinter
    canvas1.delete("all")
    # draw outline
    draw_outline(combo_shape.get())
    # draw lines
    m_actual = len(x_list)
    for n in range(m_actual):
        value = (n * p.get()) % m_actual
        if combo_color.get() == "color":
            i = int(dist([x_list[value], y_list[value]], [x_list[n], y_list[n]]) / 2)
            r = i % 256; r = min(255, r) # calculate color comp. from i
            g = i % 65 * 4; g = min(255, g)
            b = i % 128 * 2; b = min(255, b)
            col_str = f"#{r:02X}{g:02X}{b:02X}" # color in "#rrggbb" format, hex values
        else:
            col_str = combo_color.get()
        # draw line on tkinter canvas
        canvas1.create_line(x_list[value], y_list[value], x_list[n], y_list[n], fill = col_str)
        # draw line on PIL image
        draw.line([(x_list[value], y_list[value]), (x_list[n], y_list[n])], fill = col_str)
    # generate text to add
    txt = f"Modular multiplication {combo_shape.get()}, m = {m_actual}, p = {p.get()}"
    # text on tkinter canvas
    canvas1.create_text(30, 5, text = txt,
                        anchor = "nw", font = ("TkFixedFont",10,"normal"), fill = "white")
    # text on PIL image
    draw.text((30,5), txt, font = font_PIL, align = "left", fill = "white")
    update_title()
    
# update title of tkinter window
def update_title():
    root1.title(f"Modular multiplication {combo_shape.get()} using Python and tkinter, right click to save")

# export image to PNG file
def export_png():
    m_actual = int(m.get() / 4) * 4
    # define a default file name to propose, includes m and p values
    file_name = f"mod_mult_{combo_shape.get()}_{m_actual}_{p.get()}.png"
    # dialog box to confirm saving action and file name
    file_name = simpledialog.askstring("Export image as PNG", "File name:", parent = root1,
                                           initialvalue = file_name)
    # save if agreed
    if file_name is not None:
        img.save(file_name, "PNG")

# event handlers 
def click_handler(event):
    if event.num == 1: # left mouse button
        pass
    elif event.num == 3: # right mouse button
        export_png()

def combo_event_handler(event):
    draw_image(0)


    

# parameters
m_max = 600 # modulus
p_initial = 534 # value of p at startup
screen_width = 1000; screen_height = 1000
radius = 450
line_color = "white"
alpha = sin(radians(60))

# center of circle
x_center = screen_width // 2; y_center = screen_height // 2

# font to use for PIL image
font_PIL = ImageFont.truetype(r"FreeMono.ttf", 20)

# make tkinter root and canvas objects

# main window
root1 = tk.Tk()
root1.resizable(False, False)

# define tkinter variables for use with sliders
m = tk.IntVar()
m.set(m_max)
p = tk.IntVar()
p.set(p_initial)

# ttk combobox to select shape
combo_shape = ttk.Combobox(root1, values=["circle", "square", "triangle"], state = "readonly")
combo_shape.grid(row = 0, column = 0)
combo_shape.current(0)

# ttk combobox to select color
combo_color = ttk.Combobox(root1,
                           values=["color", "white", "green", "blue", "red", "yellow","cyan","magenta"],
                           state = "readonly")
combo_color.grid(row = 1, column = 0)
combo_color.current(0)

# tkinter sliders to set m and p values
slider_m = tk.Scale(root1, variable = m, label = "m", command = draw_image,
                   from_ = 2, to = m_max, orient = tk.VERTICAL, length = screen_height - 100)
slider_m.grid(row = 2, column = 0)
slider_p = tk.Scale(root1, variable = p, label = "p", command = draw_image,
                   from_ = 2, to = m.get(), orient = tk.VERTICAL, length = screen_height - 100)
slider_p.grid(row = 2, column = 1)

# canvas to draw image on
canvas1 = tk.Canvas(root1, background = "black",
                    height = screen_height, width = screen_width)
canvas1.grid(row = 0, column = 2, rowspan = 3)

# update title of main window
update_title()

# create a new PIL Image object
img = Image.new("RGB",(screen_width, screen_height),
                "black")
draw = ImageDraw.Draw(img)

# font to use for PIL image
font_PIL = ImageFont.truetype(r"FreeMono.ttf", 23)

# define event handlers 
root1.bind("<Button>", click_handler)
combo_shape.bind("<<ComboboxSelected>>", combo_event_handler)
combo_color.bind("<<ComboboxSelected>>", combo_event_handler)

# first image drawing, subsequent images are drawn when the sliders are moved
# or combo boxes modified
draw_image(0)

# tkinter main loop
root1.mainloop()

