# from tkinter import Tk

# from gui.view_student import GuessingGame


# if __name__ == "__main__":
#     root = Tk()
#     my_gui = GuessingGame(root)
#     root.mainloop()
from tkinter import *
from tkinter import ttk

from application.gui.login_screen import LoginScreen


def main():
    window = Tk()
    window.title("Student App")
    LoginScreen(window)
    window.mainloop()

main()