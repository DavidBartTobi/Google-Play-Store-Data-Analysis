
def main_grid(choose_button):

    choose_button.grid(row=0, column=0, columnspan=3, rowspan=4, pady=(0,25))


def hide_main_grid(choose_button):
    choose_button.grid_forget()


def statistic_grid(*args):

    args[0].grid(row=0, column=0, pady=(60,0))

    args[1].grid(row=0, column=1, pady=(60,0))

    args[2].grid(row=0, column=2, pady=(60,0))

    args[3].grid(row=1, column=0, pady=(10,0))

    args[4].grid(row=1, column=1, pady=(10,0))

    args[5].grid(row=1, column=2, pady=(10,0))
