from ttkthemes import ThemedStyle



def center_window(win):
    win.update_idletasks()

    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2

    return x, y


def window_style(top, title, geometry):
    top.title(title)
    top.geometry(geometry)
    top.resizable(width=False, height=False)
    w, h = center_window(top)
    top.geometry("+%d+%d" % (w, h-50))
    # ttk theme:
    style = ThemedStyle(top)
    style.set_theme('clam')


def main_theme_color():
    return '#040404'
