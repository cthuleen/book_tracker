import tkinter as tk
import sqlite

class App(tk.Tk):
    '''
    App subclass inherits from the window class of tk
    '''

    # def __init__(self):
    # 
    #   create components:
    #       + 'form' for user to input new book (title/author)
    #           - entries for user to type title & author
    #           - button to add text from entries to database
    #               > validation needed?
    #       + table for currently read
    #           - table headers (title, author)
    #           - button to finish
    #           - button to mark unfinished
    #       + table for finished
    #           - table headers (title, author)
    #           - button to begin reread (i.e. move to currently_reading)
    #       + table for unfinished
    #           - table headers (title, author)
    #           - button to begin reading again (i.e. move to currently_reading)
    #
    #
    #  other functions:
    #       + add book from form to db & tables
    #       + load books from db to tables
    # 
    #  


if __name__ == "__main__":
    app = App()
    app.mainloop()