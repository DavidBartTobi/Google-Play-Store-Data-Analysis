
def Main_Grid(choose_button):

    choose_button.grid(row=0, column=0, columnspan=3, rowspan=4, pady=(0,25))


def Hide_Main_Grid(choose_button):
    choose_button.grid_forget()


def Statistic_Grid(*args):

    args[0].grid(row=0, column=0)

    args[1].grid(row=0, column=1)

    args[2].grid(row=0, column=2)

    args[3].grid(row=1, column=0)

    args[4].grid(row=1, column=1)

    args[5].grid(row=1, column=2)
