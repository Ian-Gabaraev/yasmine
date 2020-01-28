# Class for manipulating users' private dictionaries.
import sqlite3
from datetime import datetime
from globals import path_to_user_dictionaries
from globals import sql_queries


class Notebook:
    def __init__(self, username):
        self.username = username
        self.__len = int
        self.__is_not_empty = False
        self.__current_entry = None

    # How many words are in the notebook?
    def notebook_is_not_empty(self):
        response = self.query_database_with_response(
            query=sql_queries['number of words'],
            params=[self.username],
            size='one'
        )
        self.__len = response[0]
        if self.__len > 0:
            self.__is_not_empty = True
        return self.__is_not_empty

    # This method:
    # 1. Assigns the result from retrieve_all_words(),
    # which is a list of tuples like (word, definitions, examples).
    # 2. Iterates over the list.
    # 3. Casts each tuple to list and passes it over to
    # generate_entry_for_humans().
    # 4. The latter returns a human-friendly string,
    # that is attached to string 'result'.
    def view_user_notebook(self):
        if self.notebook_is_not_empty():
            result = str()
            list_of_tuples = self.retrieve_all_words()
            for tuple in list_of_tuples:
                result += self.generate_entry_for_humans(list(tuple))
            return result
        return False

    # This method requires three arguments.
    # 1. 'query' is a string that mirrors a key i globals.sql_queries.
    # 2. 'params' is a list of parameters required to execute the query.
    # 3. 'size' denotes the size of the response object.
    # Default is 'all' - get all the results.
    # Otherwise, it returns only one result object.
    @staticmethod
    def query_database_with_response(query, params, size='all'):
        cursor = sqlite3.connect(path_to_user_dictionaries)
        try:
            response = cursor.execute(query % tuple(params))
        except sqlite3.OperationalError as error:
            # Notebook does not exist. What next?
            cursor.close()
        else:
            if size == 'all':
                result = response.fetchall()
            else:
                result = response.fetchone()
            cursor.commit()
            cursor.close()
            return result

    # ! Entry has to be sanitized to avoid SQL injections !
    def write_to_notebook(self, entry):
        word, definition, example = entry.split('&')
        if not self.notebook_has_word(word):
            current_time = datetime.now().strftime("%B %d, %Y %I:%M%p")
            # Input format: Word&Definition&Example
            self.make_void_query('add entry',
                                 [self.username, word,
                                                  definition, example,
                                                  current_time])

    # This method executes SQL queries on-demand and returns nothing.
    # Unlike m. query_database_with_response(**kwargs) that returns the result.
    @staticmethod
    def make_void_query(query, params):
        cursor = sqlite3.connect(path_to_user_dictionaries)
        sql_query = sql_queries[query] % tuple(params)
        cursor.execute(sql_query)
        cursor.commit()
        cursor.close()

    # This method tries to remove a row in the table.
    # It returns True if successful and False if the row does not exist.
    def delete_entry(self, word):
        if self.notebook_is_not_empty():
            if self.notebook_has_word(word):
                self.make_void_query('delete row', [self.username, word])
                return not self.notebook_has_word(word)
            else:
                return self.notebook_has_word(word)
        return False

    # Check if word is in the user table.
    # Return True if the row exists, else return False.
    def notebook_has_word(self, word):
        response = self.query_database_with_response(
            query=sql_queries['exists'],
            params = [self.username, word],
            size='one')
        return bool(response[0])

    def search_notebook(self, word):
        if self.notebook_is_not_empty() and self.notebook_has_word(word):
            cursor = sqlite3.connect(path_to_user_dictionaries)
            sql_query = f"SELECT word, definition, example FROM {self.username} WHERE word = %r" % word
            # Nested list comprehension.
            # It turns SQLite response which is a tuple like
            # ([word, definitions, examples])
            # into a list like [word, definitions, examples],
            # which is then assigned to private field __current_entry
            self.__current_entry = [data for entry in
                                        cursor.execute(sql_query).fetchall()
                                        for data in entry]
            cursor.close()
            return self.__current_entry
        return False

    # Turns resulting database entry into human-friendly string.
    # Accepts argument 'response' as a list of [word, definitions, examples]
    # Returns a formatted, readable string.
    @staticmethod
    def generate_entry_for_humans(response):
        return f"""
        \n
        *Word*\n{response[0]}\n
        *Definitions*\n{response[1]}\n
        *Examples*\n{response[2]}\n
        """

    # Return all the rows in the user table as a list of tuples.
    def retrieve_all_words(self):
        response = self.query_database_with_response(
            query=sql_queries['everything ordered'],
            params=[self.username],
            size='all')
        return response

    # This method creates user's notebook.
    # The columns 'exposed' and 'guessed'
    # are used to calculate how often the
    # user sees and guesses the exact word
    # during training (in %). The lower the 'rating',
    # the more often will the user encounter this
    # exact word.
    def create_notebook(self):
        command = "CREATE TABLE IF NOT EXISTS %s" \
                  "(word TEXT PRIMARY KEY," \
                  "definition TEXT," \
                  "example TEXT," \
                  "exposed INTEGER," \
                  "guessed INTEGER," \
                  "rating INTEGER," \
                  "UNIQUE(word));"
        connection = sqlite3.connect('dictionaries/vocabulary.db')
        cursor = connection.cursor()
        cursor.execute(command % self.username)
        connection.commit()
        connection.close()


n = Notebook('iangabaraev')
