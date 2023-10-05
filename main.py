from tkinter import *
from tkinter import filedialog, font
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os

# global variable for image name mostly for tkinter not to lookse the
selected_img = ""


def load_img():
    # img_to_display has to be a global variable
    # without it TKinter can't update img on canvas because something with references and garbage collector in python
    # https://stackoverflow.com/questions/67534919/can-you-change-the-picture-in-a-gui-with-a-button-press-python

    global img_to_display, selected_img

    selected_img = window.filename = filedialog.askopenfilename(initialdir="./",
                                                                title="Select file",
                                                                filetypes=(
                                                                    ("jpeg files", "*.jpg"), ("all files", "*.*")
                                                                )
                                                                )
    picture = Image.open(selected_img)

    # use thumbnail to resize img keeping aspect ratio
    picture.thumbnail((500, 420))
    img_to_display = ImageTk.PhotoImage(picture)  # use PIL to display jpg
    canvas.itemconfig(displayed_img, image=img_to_display)


def add_watermark():

    if selected_img != "":
        # source: https://www.tutorialspoint.com/python_pillow/python_pillow_creating_a_watermark.htm
        picture = Image.open(selected_img)
        width, height = picture.size
        draw = ImageDraw.Draw(picture)
        text = "picture by ghost"
        selected_font = ImageFont.truetype("arial.ttf", 30)
        # todo - place in specific place in the picture
        draw.text((10, 10), text, font=selected_font, fill="gray")

        # Save watermarked image
        # img size is smaller because PIL compresses it
        # create file name
        img_name = os.path.basename(selected_img)
        save_folder = os.path.dirname(selected_img)

        # if there are multiple dots, splitext splits at the last one
        # test.file.jpg -> ('test.file', '.jpg')
        filename_split = os.path.splitext(img_name)
        new_image_name = str(filename_split[0]) + "_watermark." + filename_split[1]

        # save img
        picture.save(os.path.join(save_folder, new_image_name))
        # todo - add status message (file saved at...)
        # todo - display watermarked img


# ------------------------------------------------
# setup tkinter window
# ------------------------------------------------
# todo - add text to customize watermarked text
window = Tk()
window.title("watermarker")
window.config(bg="teal", padx=10, pady=10)

canvas = Canvas(window, width=520, height=400, bg="teal", highlightthickness=0)
img_to_display = PhotoImage(file="./files/background_img.png")
displayed_img = canvas.create_image(10, 10, image=img_to_display, anchor="nw")
canvas.grid(column=0, row=0, columnspan=2)

button_load_img = Button(text="Load image", highlightthickness=0, command=load_img)
button_load_img.grid(column=0, row=1)

button_add_watermark = Button(text="Add watermark", highlightthickness=0, command=add_watermark)
button_add_watermark.grid(column=1, row=1)

# todo - add exit button
window.mainloop()
