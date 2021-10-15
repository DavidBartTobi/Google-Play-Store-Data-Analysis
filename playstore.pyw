from tkinter import *
from PIL import ImageTk, Image
from program import Program
import gui



root = Tk()
gui.Window_Style(root, "Google Appstore Data Analysis", "954x538")

image = Image.open('logos/logo.jpg')
image.thumbnail((950, 950))
resized_image = ImageTk.PhotoImage(image)
img_label = Label(root, image=resized_image, bg=gui.Main_Theme_Color())
img_label.grid(row=0, column=0, rowspan=4, columnspan=3)

Program(root)

root.mainloop()
