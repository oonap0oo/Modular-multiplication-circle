# Modular multiplication triangle
import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageDraw, ImageFont
from math import *


# this function draws a actual image
# output is done both on the tkinter canvas for real time viewing
# and on a PIL image to be able to export to a PNG image file later
def draw_image(slider_value):
    # calculate coordinates of points on triangle and store in lists
    x_list = []; y_list = []
    side = int(m.get() / 3) 
    for n in range(side):
        x_list.append( x_center + int(- radius + radius * n / side))
        y_list.append( y_center + int(alpha * (+ radius  - 2 * radius * n / side)))
    for n in range(side):
        x_list.append( x_center + int(radius * n / side ))
        y_list.append( y_center + int(alpha * (- radius + 2 * radius * n / side)))
    for n in range(side):
        x_list.append( x_center + int(radius  - 2 * radius * n / side))
        y_list.append( y_center + int(alpha * radius) )

        
    # clear screen tkinter
    canvas1.delete("all")
    # clear image PIL
    draw.rectangle([(0,0),(screen_width,screen_height)],fill = "black", outline = None)
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
    # draw lines
    m_actual = len(x_list)
    for n in range(m_actual):
        value = (n * p.get()) % m_actual
        # draw line on tkinter canvas
        canvas1.create_line(x_list[value], y_list[value], x_list[n], y_list[n], fill = line_color)
        # draw line on PIL image
        draw.line([(x_list[value], y_list[value]), (x_list[n], y_list[n])], fill = "white")
    # generate text to add
    txt = f"Modular multiplication triangle, m = {m_actual}, p = {p.get()}"
    # text on tkinter canvas
    canvas1.create_text(30, 5, text = txt,
                        anchor = "nw", font = ("TkFixedFont",10,"normal"), fill = "white")
    # text on PIL image
    draw.text((30,5), txt, font = font_PIL, align = "left", fill = "white")
    
# export image to PNG file
def export_png():
    m_actual = int(m.get() / 4) * 4
    file_name = f"{default_file_name}_{m_actual}_{p.get()}.png"
    file_name = simpledialog.askstring("Export image as PNG", "File name:", parent = root1,
                                           initialvalue = file_name)
    if file_name is not None:
        img.save(file_name, "PNG")

# event handler for mouse click
def click_handler(event):
    if event.num == 1: # left mouse button
        pass
    elif event.num == 3: # right mouse button
        export_png()



# parameters
m_max = 600 # modulus
screen_width = 1000; screen_height = 1000
radius = 450
line_color = "white"
default_file_name = "mod_mult_triangle"

alpha = sin(radians(60))

# center of triangle
x_center = screen_width // 2; y_center = screen_height // 2

# font to use for PIL image
font_PIL = ImageFont.truetype(r"FreeMono.ttf", 20)

# make tkinter root and canvas objects
root1 = tk.Tk()
root1.resizable(False, False)
root1.title("Modular multiplication triangle using Python and tkinter, right click to save")
m = tk.IntVar()
m.set(m_max)
p = tk.IntVar()
p.set(101)
slider_m = tk.Scale(root1, variable = m, label = "m", command = draw_image,
                   from_ = 2, to = m_max, orient = tk.VERTICAL, length = screen_height - 100)
slider_m.pack(side = tk.LEFT)
slider_p = tk.Scale(root1, variable = p, label = "p", command = draw_image,
                   from_ = 2, to = m.get(), orient = tk.VERTICAL, length = screen_height - 100)
slider_p.pack(side = tk.LEFT)
canvas1 = tk.Canvas(root1, background = "black",
                    height = screen_height, width = screen_width)
canvas1.pack()

# create a new PIL Image object
img = Image.new("RGB",(screen_width, screen_height),
                "black")
draw = ImageDraw.Draw(img)

# font to use for PIL image
font_PIL = ImageFont.truetype(r"FreeMono.ttf", 23)

# define event handler for mouse click
root1.bind("<Button>", click_handler)

# first image drawing, subsequent images are drawn when the sliders are moved
draw_image(0)

# tkinter main loop
root1.mainloop()

