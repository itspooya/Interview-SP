import sqlite3


class Database(object):
    """
    This class setups a Database object to be used with the main application
    """
    DB_LOCATION = "./database.db"

    def __init__(self):
        """
        Initialize connection as conn
        Cursor as cursor
        Create table function as create_table
        """
        self.conn = sqlite3.connect(self.DB_LOCATION)
        self.cursor = self.conn.cursor()
        self.create_table()

    def close(self):
        """
        Closes the connection
        :return: None
        """
        self.conn.close()

    def execute(self, new_query):
        """
        This function executes a query
        :param new_query: SQL QUERY to be executed
        :return: None
        """
        self.cursor.execute(new_query)

    def create_table(self):
        """
        This function creates 3 tables in the database
        :return: None
        """
        self.execute("""
            CREATE TABLE IF NOT EXISTS allocations(
                id INTEGER PRIMARY KEY,
                chip INTEGER,
                bot INTEGER
            )
        """)
        self.execute("""
                    CREATE TABLE IF NOT EXISTS bots(
                        bot_id INTEGER PRIMARY KEY,
                        chip_1_value INTEGER ,
                        chip_2_value INTEGER
                    )
                """)
        self.execute("""
        CREATE TABLE IF NOT EXISTS outputs(output_id INTEGER PRIMARY KEY,
        chip_value INTEGER)""")

    def commit(self):
        """
        This function commits the changes to the database
        :return:
        """
        self.conn.commit()
