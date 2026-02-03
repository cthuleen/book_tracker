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
        self.frm_tables.grid(row=1, column=0, padx=10)

        # Frames for the submission and edit forms
        self.frm_form_submit = tk.Frame(self.frm_form)
        self.frm_form_edit = tk.Frame(self.frm_form)

        self.frm_form_submit.grid(row=0, column=0, padx=20, pady=10)
        self.frm_form_edit.grid(row=0, column=1, padx=20, pady=10)

        # Frames for each section: reading, unfinished, & finished
        self.frm_reading = tk.Frame(self.frm_tables)
        self.frm_unfinished = tk.Frame(self.frm_tables)
        self.frm_finished = tk.Frame(self.frm_tables)

        self.frm_reading.grid(row=0, column=0, padx=5)
        self.frm_unfinished.grid(row=0, column=1, padx=5)
        self.frm_finished.grid(row=0, column=2, padx=5)
        
        # Subframes for reading
        self.frm_reading_lbl = tk.Frame(self.frm_reading)
        self.frm_reading_tree = tk.Frame(self.frm_reading)
        self.frm_reading_btns = tk.Frame(self.frm_reading)
        
        self.frm_reading_lbl.grid(row=0, column=0)
        self.frm_reading_tree.grid(row=1, column=0, pady=5)
        self.frm_reading_btns.grid(row=2, column=0, pady=5)
        

        # Subframes for unfinished
        self.frm_unfinished_lbl = tk.Frame(self.frm_unfinished)
        self.frm_unfinished_tree = tk.Frame(self.frm_unfinished)
        self.frm_unfinished_btns = tk.Frame(self.frm_unfinished)

        self.frm_unfinished_lbl.grid(row=0, column=0)
        self.frm_unfinished_tree.grid(row=1, column=0, pady=5)
        self.frm_unfinished_btns.grid(row=2, column=0, pady=5)


        # Subframes for finished
        self.frm_finished_lbl = tk.Frame(self.frm_finished)
        self.frm_finished_tree = tk.Frame(self.frm_finished)
        self.frm_finished_btns = tk.Frame(self.frm_finished)

        self.frm_finished_lbl.grid(row=0, column=0)
        self.frm_finished_tree.grid(row=1, column=0, pady=5)
        self.frm_finished_btns.grid(row=2, column=0, pady=5)

        
        # Submit form
        # widgets for the book submission form (two label/entry pairs and a button)
        self.lbl_title = tk.Label(master=self.frm_form_submit, text="Enter book title:")
        self.ent_title = tk.Entry(master=self.frm_form_submit, width=20)

        self.lbl_author = tk.Label(master=self.frm_form_submit, text="Enter book author:")
        self.ent_author = tk.Entry(master=self.frm_form_submit, width=20)

        self.btn_form = tk.Button(master=self.frm_form_submit, text="Add", command=self.submit)

        self.lbl_title.grid(row=0, column=0, pady=5, sticky="E")
        self.ent_title.grid(row=0, column=1, pady=5)
        self.lbl_author.grid(row=1, column=0, sticky="E")
        self.ent_author.grid(row=1, column=1)

        self.btn_form.grid(row=2, column=1, sticky="EW", pady=5)


        # Edit frame
        self.lbl_selected_title = tk.Label(master=self.frm_form_edit, text="Selected book title:")
        self.ent_selected_title = tk.Entry(master=self.frm_form_edit, width=20)

        self.lbl_selected_author = tk.Label(master=self.frm_form_edit, text="Selected book author:")
        self.ent_selected_author = tk.Entry(master=self.frm_form_edit, width=20)

        self.btn_form_edit = tk.Button(master=self.frm_form_edit, text="Change")

        self.lbl_selected_title.grid(row=0, column=0, pady=5, sticky="E")
        self.ent_selected_title.grid(row=0, column=1, pady=5)
        self.lbl_selected_author.grid(row=1, column=0, sticky="E")
        self.ent_selected_author.grid(row=1, column=1)

        self.btn_form_edit.grid(row=2, column=1, sticky="EW", pady=5)


        # Reading
        # currently reading table frame
        self.lbl_reading = tk.Label(master=self.frm_reading_lbl, text="Currently Reading")
        self.btn_reading_to_unfinished = tk.Button(master=self.frm_reading_btns, text="Mark unfinished?", command=self.mark_unfinished)
        self.btn_reading_to_finished = tk.Button(master=self.frm_reading_btns, text="Mark finished?", command=self.mark_finished)

        # Scrollbar for tree
        self.reading_scrollbar = ttk.Scrollbar(self.frm_reading_tree, orient="vertical")

        # Define columns 
        columns = ('book_title', 'book_author')
        self.reading_tree = ttk.Treeview(self.frm_reading_tree, columns=columns, 
                                         show='headings', yscrollcommand=self.reading_scrollbar,
                                         selectmode='browse') # 'show="headings"' hides the default #0 column
        self.reading_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Define headings
        self.reading_tree.heading('book_title', text='Title')
        self.reading_tree.heading('book_author', text='Author')

        self.reading_scrollbar.configure(command=self.reading_tree.yview)
        


        # Unfinished
        # unfinished table frame
        self.lbl_unfinished = tk.Label(master=self.frm_unfinished_lbl, text="Unfinished Books")
        self.btn_unfinished_to_reading = tk.Button(master=self.frm_unfinished_btns, text="Begin Reading?", command=self.begin_reading)

        # Scrollbar for tree
        self.unfinished_scrollbar = ttk.Scrollbar(self.frm_unfinished_tree, orient="vertical")

        # Define columns 
        columns = ('book_title', 'book_author')
        self.unfinished_tree = ttk.Treeview(self.frm_unfinished_tree, columns=columns, 
                                            show='headings', yscrollcommand=self.unfinished_scrollbar.set,
                                            selectmode='browse') 
        self.unfinished_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Define headings
        self.unfinished_tree.heading('book_title', text='Title')
        self.unfinished_tree.heading('book_author', text='Author')

        self.unfinished_scrollbar.configure(command=self.unfinished_tree.yview)



        #Finished
        # finished label and button
        self.lbl_finished = tk.Label(master=self.frm_finished_lbl, text="Finished Books")
        self.btn_finished_to_reading = tk.Button(master=self.frm_finished_btns, text="Reread?", command=self.reread)

        # Scrollbar for tree
        self.finished_scrollbar = ttk.Scrollbar(self.frm_finished_tree, orient="vertical")

        # finished tree
        columns = ('book_title', 'book_author')
        self.finished_tree = ttk.Treeview(self.frm_finished_tree, columns=columns, 
                                          show='headings', yscrollcommand=self.finished_scrollbar.set,
                                          selectmode='browse')
        self.finished_tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Define headings
        self.finished_tree.heading('book_title', text='Title')
        self.finished_tree.heading('book_author', text='Author')

        self.finished_scrollbar.configure(command=self.finished_tree.yview)

        


        # load books from db into tables
        self.load()

        self.lbl_reading.grid(row=0, column=0, pady=5)
        self.btn_reading_to_unfinished.grid(row=0, column=0, padx=10)
        self.btn_reading_to_finished.grid(row=0, column=1)
        self.reading_tree.grid(row=0, column=0)
        self.reading_scrollbar.grid(row=0, column=1)


        self.lbl_unfinished.grid(row=0, column=0, pady=5)
        self.btn_unfinished_to_reading.grid(row=0, column=0, padx=10)
        self.unfinished_tree.grid(row=0, column=0)
        self.unfinished_scrollbar.grid(row=0, column=1)


        self.lbl_finished.grid(row=0, column=0, pady=5)
        self.btn_finished_to_reading.grid(row=0, column=0, padx=10)
        self.finished_tree.grid(row=0, column=0)
        self.finished_scrollbar.grid(row=0, column=1)


    def on_tree_select(self, event):
        ''' allow only one entry to be selected among all tables at a given moment'''
        

        current_tree = event.widget

        selected_items = current_tree.selection()
        
        # Clear the other two trees of their selection
        # Ensures that the following code won't execute as part of any of the following selection shenanigans
        if selected_items: 

            if current_tree == self.reading_tree:
                self.unfinished_tree.selection_remove(self.unfinished_tree.selection())
                self.finished_tree.selection_remove(self.finished_tree.selection())
                item_values = self.reading_tree.item(selected_items[0], 'values')

            if current_tree == self.unfinished_tree:
                self.reading_tree.selection_remove(self.reading_tree.selection())
                self.finished_tree.selection_remove(self.finished_tree.selection())
                item_values = self.unfinished_tree.item(selected_items[0], 'values')

            if current_tree == self.finished_tree:
                self.reading_tree.selection_remove(self.reading_tree.selection())
                self.unfinished_tree.selection_remove(self.unfinished_tree.selection())
                item_values = self.finished_tree.item(selected_items[0], 'values')


            

            # Update the edit form's text
            title = item_values[0]
            author = item_values[1]

            self.ent_selected_author.delete(0, tk.END)
            self.ent_selected_title.delete(0, tk.END)

            self.ent_selected_author.insert(0, author)
            self.ent_selected_title.insert(0, title)

    

    def submit(self):
        ''' add book from form to database, marking it as unfinished, and add it to the unfinshed table '''

        title = self.ent_title.get().strip()        # clear leading and trailing whitespace
        author = self.ent_author.get().strip()

        # check to make sure neither title nor author is empty
        if title == "" or author == "":
            print("Title and author must be non-empty")
            return

        was_successful = sqlite.insert_book(title, author)

        if was_successful: 
            self.unfinished_tree.insert('', tk.END, values=(title, author))

            # clear the form entries
            self.ent_title.delete(0, tk.END)
            self.ent_author.delete(0, tk.END)

        

    def load(self):
        ''' load books from db into tables'''
        currently_reading, finished, unfinished = sqlite.fetch()

        for book in currently_reading:
            self.reading_tree.insert('', tk.END, values=(book[1], book[2]))

        for book in unfinished:
            self.unfinished_tree.insert('', tk.END, values=(book[1], book[2]))

        for book in finished:
            self.finished_tree.insert('', tk.END, values=(book[1], book[2]))


    # Function for books in unfinished
    def begin_reading(self):
        selected_item = self.unfinished_tree.selection() # returns tuple of selected item id's

        if selected_item:
            item_id = selected_item[0]
            item_data = self.unfinished_tree.item(item_id, 'values') # returns tuple of book's title and author

            self.unfinished_tree.delete(item_id)
            self.reading_tree.insert('', tk.END, values=(item_data[0], item_data[1]))

            sqlite.start_reading(item_data[0], item_data[1])

    # Function for books in finished
    def reread(self):
        selected_item = self.finished_tree.selection() 

        if selected_item:
            item_id = selected_item[0]
            item_data = self.finished_tree.item(item_id, 'values') 

            self.finished_tree.delete(item_id)
            self.reading_tree.insert('', tk.END, values=(item_data[0], item_data[1]))

            sqlite.start_reading(item_data[0], item_data[1])


    # Functions for books in Reading
    def mark_unfinished(self):
        selected_item = self.reading_tree.selection()

        if selected_item:
            item_id = selected_item[0]
            item_data = self.reading_tree.item(item_id, 'values') 

            self.reading_tree.delete(item_id)
            self.unfinished_tree.insert('', tk.END, values=(item_data[0], item_data[1]))

            sqlite.mark_unfinished(item_data[0], item_data[1])

    
    def mark_finished(self):
        selected_item = self.reading_tree.selection() 

        if selected_item:
            item_id = selected_item[0]
            item_data = self.reading_tree.item(item_id, 'values') 

            self.reading_tree.delete(item_id)
            self.finished_tree.insert('', tk.END, values=(item_data[0], item_data[1]))

            sqlite.mark_finished(item_data[0], item_data[1])


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