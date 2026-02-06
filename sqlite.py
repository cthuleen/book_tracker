import sqlite3

def create_table():
    ''' Create the Book table, if it doesn't exist '''

    with sqlite3.connect('db/my_database.db') as connection:

        cursor = connection.cursor()

        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_reading TEXT NOT NULL,
            times_read INTEGER NOT NULL
        );
        '''

        cursor.execute(create_table_query)

        connection.commit()

        print("Database created and/or connected successfully!")



def insert_book(title, author):
    ''' 
        Add a new record to the Book table, if it is a unique author/title pair

        Returns False if not valid input, and True otherwise
    '''

    with sqlite3.connect('db/my_database.db') as connection:

        # check to make sure book hasn't already been inserted
        # NB: book titles are allowed to repeat across authors, but not for the same author

        books_by_author = fetch_books_by_author(author)

        for book in books_by_author:

            existing_title = book[1]

            if title == existing_title:
                print("Book already exists!")
                return False


        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO Books (title, author, is_reading, times_read) 
        VALUES (?, ?, ?, ?);
        '''

        # initialize is_reading to "NO" and times_read to 0
        book_tuple = (title, author, "NO", 0)

        cursor.execute(insert_query, book_tuple)

        connection.commit()

        print("Record inserted successfully!")
        return True


def update_book(old_title, old_author, new_title, new_author):
    ''' 
        Update the title, author, or both of a book record 

        Must not violate the author/title pair uniqueness rule    
    '''

    with sqlite3.connect('db/my_database.db') as connection:
        cursor = connection.cursor()

        # validate input...
        # NB: book titles are allowed to repeat across authors, but not for the same author

        books_by_author = fetch_books_by_author(new_author)

        for book in books_by_author:

            existing_title = book[1]

            if new_title == existing_title:
                print("Book already exists!")
                return False


        update_query = '''
        UPDATE Books 
        SET title = ?, author = ?
        WHERE title = ? AND author = ?;
        '''

        cursor.execute(update_query, (new_title, new_author, old_title, old_author))

        connection.commit()

        print(f"Updated {old_title} by {old_author} to {new_title} by {new_author}")
        return True


def start_reading(title, author):
    ''' Update is_reading of a book from NO to YES '''

    with sqlite3.connect('db/my_database.db') as connection:
        cursor = connection.cursor()

        update_query = '''
        UPDATE Books 
        SET is_reading = ? 
        WHERE title = ? AND author = ?;
        '''

        cursor.execute(update_query, ("YES", title, author))

        connection.commit()

        print(f"Updated reading status for {title} by {author} to YES.")


def didnt_finish(title, author):
    ''' Update is_reading of a book from YES to NO '''

    with sqlite3.connect('db/my_database.db') as connection:
        cursor = connection.cursor()

        update_query = '''
        UPDATE Books 
        SET is_reading = ? 
        WHERE title = ? AND author = ?;
        '''

        cursor.execute(update_query, ("NO", title, author))

        connection.commit()

        print(f"Updated reading status for {title} by {author} to NO.")


def did_finish(title, author):
    ''' Update is_reading of a book from YES to NO and increment times_read'''

    with sqlite3.connect('db/my_database.db') as connection:
        cursor = connection.cursor()

        update_query = '''
        UPDATE Books 
        SET is_reading = ?,  times_read = times_read + 1
        WHERE title = ? AND author = ?;
        '''

        cursor.execute(update_query, ("NO",title, author))

        connection.commit()

        print(f"Updated reading status for {title} by {author} to NO.")


def fetch_book(title, author):
    ''' fetch a single book from the table, if it exists'''

    with sqlite3.connect('db/my_database.db') as connection:

        cursor = connection.cursor()

        select_authors_books= "SELECT * FROM Books WHERE title = ? AND author = ?;"
        cursor.execute(select_authors_books, (title, author))
        book = cursor.fetchall()

        return book
    

def fetch():
    '''
        Fetch all records from Book table, then sort them into the three divisions

        Currently Reading: books that are currently being read
        Finished: books that have been finished at least once and are not being read currently
        Unfinished: books that have never been finished and are not being read currently
    '''

    with sqlite3.connect('db/my_database.db') as connection:

        cursor = connection.cursor()

        # Currently reading
        select_currently_reading = "SELECT * FROM Books WHERE is_reading = 'YES';"
        cursor.execute(select_currently_reading)
        currently_reading = cursor.fetchall()

        # Finished
        select_finished = "SELECT * FROM Books WHERE is_reading = 'NO' AND times_read > 0;"
        cursor.execute(select_finished)
        finished = cursor.fetchall()

        # Unfinished
        select_unfinished = "SELECT * FROM Books WHERE is_reading = 'NO' AND times_read = 0;"
        cursor.execute(select_unfinished)
        unfinished = cursor.fetchall()

        return (currently_reading, finished, unfinished)


def fetch_books_by_author(author):
    ''' fetch all books by an author '''

    with sqlite3.connect('db/my_database.db') as connection:

        cursor = connection.cursor()

        select_authors_books= "SELECT * FROM Books WHERE author = ?;"
        cursor.execute(select_authors_books, (author, ))
        authors_books = cursor.fetchall()

        return authors_books