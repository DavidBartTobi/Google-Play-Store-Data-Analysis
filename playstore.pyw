from tkinter import *
from PIL import ImageTk, Image
from program import Program
import gui

def main():

    root = Tk()
    gui.window_style(root, "Google Appstore Data Analysis", "692x390")

    image = Image.open('logos/logo2.jpg')
    image.thumbnail((690, 690))
    resized_image = ImageTk.PhotoImage(image)
    img_label = Label(root, image=resized_image, bg=gui.main_theme_color())
    img_label.grid(row=0, column=0, rowspan=3, columnspan=3)

    Program(root)

    root.mainloop()


if __name__ == '__main__':
    main()