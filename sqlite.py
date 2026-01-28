import sqlite3

def create_table():
    # Use 'with' to connect to the SQLite database and automatically close the connection when done
    with sqlite3.connect('db/my_database.db') as connection:

        # Create a cursor object
        cursor = connection.cursor()

        # Write the SQL command to create the Book table
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            is_reading TEXT NOT NULL,
            times_read INTEGER NOT NULL
        );
        '''

        # Execute the SQL command
        cursor.execute(create_table_query)

        connection.commit()

        print("Database created and connected successfully!")

    # No need to call connection.close(); it's done automatically!


def insert_book(title, author):

    # Use 'with' to open and close the connection automatically
    with sqlite3.connect('db/my_database.db') as connection:
        cursor = connection.cursor()

        # Insert a record into the Students table
        insert_query = '''
        INSERT INTO Books (title, author, is_reading, times_read) 
        VALUES (?, ?, ?, ?);
        '''

        # the '?' are placeholders into which the following tuple will be passed
        # this is done to prevent SQL injection

        # initialize is_reading to "NO" and times_read to 0
        book_tuple = (title, author, "NO", 0)

        cursor.execute(insert_query, book_tuple)

        # Commit the changes automatically
        connection.commit()

        # No need to call connection.close(); it's done automatically!
        print("Record inserted successfully!")


def fetch():
    # Use 'with' to connect to the SQLite database
    with sqlite3.connect('db/my_database.db') as connection:

        # Create a cursor object
        cursor = connection.cursor()


        # SQL command to select book records that are currently being read
        select_currently_reading = "SELECT * FROM Books WHERE is_reading = 'YES';"
        cursor.execute(select_currently_reading)

        # Fetch all returned records
        currently_reading = cursor.fetchall()


        # SQL command to select book records that have been finished (and aren't currently being read)
        select_finished = "SELECT * FROM Books WHERE is_reading = 'NO' AND times_read > 0;"
        cursor.execute(select_finished)

        # Fetch all returned records
        finished = cursor.fetchall()


        # SQL command to select book records that are unfinished (and not currently being read)
        select_unfinished = "SELECT * FROM Books WHERE is_reading = 'NO' AND times_read = 0;"
        cursor.execute(select_unfinished)

        # Fetch all returned records
        unfinished = cursor.fetchall()

        return (currently_reading, finished, unfinished)


        

        