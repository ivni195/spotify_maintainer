import sqlite3


class DBHandler:
    def __init__(self):
        self._connection: sqlite3.Connection = self.connect_to_database()

    def connect_to_database(self) -> sqlite3.Connection:
        try:
            print('Succesfully opened the database.')
            return sqlite3.connect('spfmaint.db')
        except:
            print('Error occured when opening the database.')
            exit(-1)

    def check_table_existance(self, table_name: str) -> bool:
        result = self._connection.execute(f"""
        SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';
        """)
        return result.fetchone() is not None

    def create_table(self, table_name: str):
        self._connection.execute(f"""
            CREATE TABLE '{table_name}'(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                ARTIST          TEXT      NOT NULL,
                NAME            INT       NOT NULL,
                DOWNLOADED      INT       NOT NULL
            );
        """)

    def insert_record(self, table_name: str, artist: str, name: str):
        self._connection.execute(f"""
            INSERT INTO '{table_name}' (ARTIST, NAME, DOWNLOADED)
            VALUES ('{artist}', '{name}', 0);
        """)

    def mark_as_downloaded(self, table_name: str, id: int):
        self._connection.execute(f"""
            UPDATE {table_name} SET DOWNLOADED=1 WHERE ID={id};
        """)

    def find_all_not_downloaded(self, table_name: str) -> list:
        results = self._connection.execute(f"""
            SELECT * FROM {table_name} WHERE DOWNLOADED=0
        """)
        return results.fetchall()

    def test_fetch(self):
        result = self._connection.execute('SELECT * FROM test;')
        print(result.fetchall())

    def commit(self):
        self._connection.commit()