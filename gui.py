import tkinter as tk        # for classic widgets
from tkinter import ttk     # for themed (i.e. modern) widgets
import sqlite

class App(tk.Tk):
    '''
    App subclass inherits from the window class of tk
    '''

    def __init__(self):
        ''' add description here '''

        tk.Tk.__init__(self)
        self.title("Reading Tracker")

        # create DB and table if needed
        sqlite.create_table()

        # init frames and the window's columns
        self.frm_form = tk.Frame(self)
        self.frm_tables = tk.Frame(self)

        self.frm_form.grid(row=0, column=0)
        self.frm_tables.grid(row=0, column=1, padx=20)

        # widgets for the book submission form (two label/entry pairs and a button)
        self.lbl_title = tk.Label(master=self.frm_form, text="Enter book title:")
        self.ent_title = tk.Entry(master=self.frm_form, width=20)

        self.lbl_author = tk.Label(master=self.frm_form, text="Enter book author:")
        self.ent_author = tk.Entry(master=self.frm_form, width=20)

        self.btn_form = tk.Button(master=self.frm_form, text="Add", command=self.submit)

        self.lbl_title.grid(row=0, column=0, pady=5, sticky="E")
        self.ent_title.grid(row=0, column=1, pady=5)
        self.lbl_author.grid(row=1, column=0, sticky="E")
        self.ent_author.grid(row=1, column=1)

        self.btn_form.grid(row=2, column=1, sticky="EW", pady=5)

        # unfinished table frame
        self.lbl_unfinished = tk.Label(master=self.frm_tables, text="Unfinished Books")

        # Define columns (the first column '#0' is the default tree column)
        columns = ('book_title', 'book_author', 'begin_again')
        self.tree = ttk.Treeview(self.frm_tables, columns=columns, show='headings') # 'show="headings"' hides the default #0 column

        # Define headings
        self.tree.heading('book_title', text='Title')
        self.tree.heading('book_author', text='Author')
        self.tree.heading('begin_again', text='Begin Again?')

        # load books from db into tables
        self.load()

        self.lbl_unfinished.grid(row=0, column=0, pady=5)
        self.tree.grid(row=1, column=0)


        


    
    def submit(self):
        ''' add book from form to database'''

        title = self.ent_title.get()
        author = self.ent_author.get()

        sqlite.insert_book(title, author)

    def load(self):
        ''' load books from db into tables'''
        currently_reading, finished, unfinished = sqlite.fetch()

        for book in unfinished:
            self.tree.insert('', tk.END, values=(book[1], book[2], "TBD"))

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