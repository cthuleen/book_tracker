import tkinter as tk        # for classic widgets
from tkinter import ttk     # for themed (i.e. modern) widgets
import sqlite

class App(tk.Tk):
    '''
    App subclass inherits from the window class of tk
    '''

    def __init__(self):
        ''' 
            Initialize the database and set up the app window
            
            App comprises:
                - submission form
                - edit form
                - Currently reading table + buttons
                - Unfinished table + button
                - Finished table + button
        '''

        tk.Tk.__init__(self)
        self.title("Reading Tracker")

        # create DB and table if needed
        sqlite.create_table()

        # init form and table frames
        self.frm_form = tk.Frame(self)
        self.frm_tables = tk.Frame(self)

        self.frm_form.grid(row=0, column=0)
        self.frm_tables.grid(row=1, column=0, padx=10)


        # Submission and Edit Forms

        # Frames 
        self.frm_form_submit = tk.Frame(self.frm_form)
        self.frm_form_edit = tk.Frame(self.frm_form)

        self.frm_form_submit.grid(row=0, column=0, padx=20, pady=10)
        self.frm_form_edit.grid(row=0, column=1, padx=20, pady=10)

        # Submit form widgets
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


        # Edit frame widgets
        self.lbl_selected_title = tk.Label(master=self.frm_form_edit, text="Selected book title:")
        self.ent_selected_title = tk.Entry(master=self.frm_form_edit, width=20)

        self.lbl_selected_author = tk.Label(master=self.frm_form_edit, text="Selected book author:")
        self.ent_selected_author = tk.Entry(master=self.frm_form_edit, width=20)

        self.btn_form_edit = tk.Button(master=self.frm_form_edit, text="Change", command=self.change)

        self.lbl_selected_title.grid(row=0, column=0, pady=5, sticky="E")
        self.ent_selected_title.grid(row=0, column=1, pady=5)
        self.lbl_selected_author.grid(row=1, column=0, sticky="E")
        self.ent_selected_author.grid(row=1, column=1)

        self.btn_form_edit.grid(row=2, column=1, sticky="EW", pady=5)


        # Book tables

        # Frames for each book section: reading, unfinished, & finished
        self.frm_reading = tk.Frame(self.frm_tables)
        self.frm_unfinished = tk.Frame(self.frm_tables)
        self.frm_finished = tk.Frame(self.frm_tables)

        self.frm_reading.grid(row=0, column=0, padx=5)
        self.frm_unfinished.grid(row=0, column=1, padx=5)
        self.frm_finished.grid(row=0, column=2, padx=5)
        
        # Subframes for reading lbl, tree, and btns
        self.frm_reading_lbl = tk.Frame(self.frm_reading)
        self.frm_reading_tree = tk.Frame(self.frm_reading)
        self.frm_reading_btns = tk.Frame(self.frm_reading)
        
        self.frm_reading_lbl.grid(row=0, column=0)
        self.frm_reading_tree.grid(row=1, column=0, pady=5)
        self.frm_reading_btns.grid(row=2, column=0, pady=5)
        

        # Subframes for unfinished lbl, tree, and btn
        self.frm_unfinished_lbl = tk.Frame(self.frm_unfinished)
        self.frm_unfinished_tree = tk.Frame(self.frm_unfinished)
        self.frm_unfinished_btns = tk.Frame(self.frm_unfinished)

        self.frm_unfinished_lbl.grid(row=0, column=0)
        self.frm_unfinished_tree.grid(row=1, column=0, pady=5)
        self.frm_unfinished_btns.grid(row=2, column=0, pady=5)


        # Subframes for finished lbl, tree, and btn
        self.frm_finished_lbl = tk.Frame(self.frm_finished)
        self.frm_finished_tree = tk.Frame(self.frm_finished)
        self.frm_finished_btns = tk.Frame(self.frm_finished)

        self.frm_finished_lbl.grid(row=0, column=0)
        self.frm_finished_tree.grid(row=1, column=0, pady=5)
        self.frm_finished_btns.grid(row=2, column=0, pady=5)


        # Reading
        # currently reading table frame
        self.lbl_reading = tk.Label(master=self.frm_reading_lbl, text="Currently Reading")
        self.btn_reading_to_unfinished = tk.Button(master=self.frm_reading_btns, text="Mark unfinished?", command=self.didnt_finish)
        self.btn_reading_to_finished = tk.Button(master=self.frm_reading_btns, text="Mark finished?", command=self.did_finish)

        # Scrollbar for tree
        self.reading_scrollbar = ttk.Scrollbar(self.frm_reading_tree, orient="vertical")

        # Define columns 
        columns = ('book_title', 'book_author')
        self.reading_tree = ttk.Treeview(self.frm_reading_tree, columns=columns, 
                                         show='headings', yscrollcommand=self.reading_scrollbar,
                                         selectmode='browse') # 'show="headings"' hides the default #0 column
        
        # bind the on_tree_select fn to both click and double click, meaning a double click will quickly select then unselect an item
        self.reading_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.reading_tree.bind('<Double-1>', self.on_tree_select) 

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
        
        # bind the on_tree_select fn to both click and double click, meaning a double click will quickly select then unselect an item
        self.unfinished_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.unfinished_tree.bind('<Double-1>', self.on_tree_select) 

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
        
        # bind the on_tree_select fn to both click and double click, meaning a double click will quickly select then unselect an item
        self.finished_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.finished_tree.bind('<Double-1>', self.on_tree_select) 

        # Define headings
        self.finished_tree.heading('book_title', text='Title')
        self.finished_tree.heading('book_author', text='Author')

        self.finished_scrollbar.configure(command=self.finished_tree.yview)


        # load books from db into tables
        self.load()


        # Place widgets of Currently Reading section in their respective subframes
        self.lbl_reading.grid(row=0, column=0, pady=5)
        self.btn_reading_to_unfinished.grid(row=0, column=0, padx=10)
        self.btn_reading_to_finished.grid(row=0, column=1)
        self.reading_tree.grid(row=0, column=0)
        self.reading_scrollbar.grid(row=0, column=1)

        # Place widgets of Unfinished section in their respective subframes
        self.lbl_unfinished.grid(row=0, column=0, pady=5)
        self.btn_unfinished_to_reading.grid(row=0, column=0, padx=10)
        self.unfinished_tree.grid(row=0, column=0)
        self.unfinished_scrollbar.grid(row=0, column=1)

        # Place widgets of Finished section in their respective subframes
        self.lbl_finished.grid(row=0, column=0, pady=5)
        self.btn_finished_to_reading.grid(row=0, column=0, padx=10)
        self.finished_tree.grid(row=0, column=0)
        self.finished_scrollbar.grid(row=0, column=1)

        # variables for on_tree_select, or should they default to empty string?
        self.selected_title = None
        self.selected_author = None


    def on_tree_select(self, event):
        ''' On table entry click, clear the previous table of its selection to enforce only one selection across all tables at a time'''

        current_tree = event.widget

        selected_items = current_tree.selection()

        reselection = False
        
        # Clear the other two trees of their selection
        # If statement ensures that the following code won't execute as part of any of the following selection shenanigans
        if selected_items: 

            if current_tree == self.reading_tree:

                self.unfinished_tree.selection_remove(self.unfinished_tree.selection())
                self.finished_tree.selection_remove(self.finished_tree.selection())
                item_values = self.reading_tree.item(selected_items[0], 'values')

                # check if reselected current selection, and delete if so
                if self.selected_author == item_values[1] and self.selected_title == item_values[0]:

                    self.reading_tree.selection_remove(self.reading_tree.selection())
                    reselection = True


            if current_tree == self.unfinished_tree:
                self.reading_tree.selection_remove(self.reading_tree.selection())
                self.finished_tree.selection_remove(self.finished_tree.selection())
                item_values = self.unfinished_tree.item(selected_items[0], 'values')

                if self.selected_author == item_values[1] and self.selected_title == item_values[0]:

                    self.unfinished_tree.selection_remove(self.unfinished_tree.selection())
                    reselection = True

            if current_tree == self.finished_tree:
                self.reading_tree.selection_remove(self.reading_tree.selection())
                self.unfinished_tree.selection_remove(self.unfinished_tree.selection())
                item_values = self.finished_tree.item(selected_items[0], 'values')

                if self.selected_author == item_values[1] and self.selected_title == item_values[0]:

                    self.finished_tree.selection_remove(self.finished_tree.selection())
                    reselection = True


            # Update the edit form's text to display selected entry's title and author
            self.ent_selected_author.delete(0, tk.END)
            self.ent_selected_title.delete(0, tk.END)
            
            if reselection:
                title = ""
                author = ""
            else:
                title = item_values[0]
                author = item_values[1]

            self.ent_selected_author.insert(0, author)
            self.ent_selected_title.insert(0, title)

            self.selected_author = author
            self.selected_title = title

    

    def submit(self):
        ''' add book from submit form to database, marking it as unfinished, and add it to the unfinshed table '''

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


    def change(self):
        ''' change the selected book's title, author, or both based on edit form; if the DB update clears, update the tree entry, too'''

        title = self.ent_selected_title.get().strip()        # clear leading and trailing whitespace
        author = self.ent_selected_author.get().strip()

        # check if title or author is empty
        if title == "" or author == "":
            print("Title and author must be non-empty")
            return
        

        # Determine which tree the selection is from, and update the entry in said tree

        # Reading tree
        reading_item_id = self.reading_tree.selection()

        if reading_item_id:
            values = self.reading_tree.item(reading_item_id[0])['values']

            was_successful = sqlite.update_book(values[0], values[1], title, author)

            if was_successful:
                self.reading_tree.item(reading_item_id[0], values=(title, author))

                # clear the form entries
                self.ent_title.delete(0, tk.END)
                self.ent_author.delete(0, tk.END)


        # Unfinished tree
        unfinished_item_id = self.unfinished_tree.selection()

        if unfinished_item_id:
            values = self.unfinished_tree.item(unfinished_item_id[0])['values']

            was_successful = sqlite.update_book(values[0], values[1], title, author)

            if was_successful:
                self.unfinished_tree.item(unfinished_item_id[0], values=(title, author))

                # clear the form entries
                self.ent_title.delete(0, tk.END)
                self.ent_author.delete(0, tk.END)


        # Finished tree
        finished_item_id = self.finished_tree.selection()

        if finished_item_id:
            values = self.finished_tree.item(finished_item_id[0])['values']

            was_successful = sqlite.update_book(values[0], values[1], title, author)

            if was_successful:
                self.finished_tree.item(finished_item_id[0], values=(title, author))

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
    def didnt_finish(self):
        ''' if the book has been finished before, it goes back to finished; else it goes back to unfinished'''
        selected_item = self.reading_tree.selection()

        if selected_item:
            item_id = selected_item[0]
            item_data = self.reading_tree.item(item_id, 'values') 

            self.reading_tree.delete(item_id)

            book = sqlite.fetch_book(item_data[0], item_data[1])[0] # get the only book returned from the set
            times_read = book[4]

            if times_read == 0:
                self.unfinished_tree.insert('', tk.END, values=(item_data[0], item_data[1]))
            else:
                self.finished_tree.insert('', tk.END, values=(item_data[0], item_data[1]))


            sqlite.didnt_finish(item_data[0], item_data[1])

    
    def did_finish(self):
        selected_item = self.reading_tree.selection() 

        if selected_item:
            item_id = selected_item[0]
            item_data = self.reading_tree.item(item_id, 'values') 

            self.reading_tree.delete(item_id)
            self.finished_tree.insert('', tk.END, values=(item_data[0], item_data[1]))

            sqlite.did_finish(item_data[0], item_data[1])


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