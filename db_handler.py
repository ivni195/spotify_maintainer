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
        SELECT name FROM sqlite_master WHERE type='table' AND name=?;
        """, (table_name,))
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

    def insert_song(self, table_name: str, artist: str, name: str):

        self._connection.execute(f"""
            INSERT INTO {table_name} (ARTIST, NAME, DOWNLOADED) VALUES (?, ?, 0);
        """, (artist, name))

    def mark_as_downloaded(self, table_name: str, id: int):

        self._connection.execute(f"""
            UPDATE {table_name} SET DOWNLOADED=1 WHERE ID=?;
        """, (id,))

    def get_all_not_downloaded(self, table_name: str) -> list:
        results = self._connection.execute(f"""
            SELECT * FROM {table_name} WHERE DOWNLOADED=0
        """)
        return results.fetchall()

    def get_table_info(self, table_name: str) -> tuple:
        """:return: (downloaded songs, total songs)"""

        total_result = self._connection.execute(f"""
            SELECT * FROM {table_name};
        """)
        total = len(total_result.fetchall())

        downloaded_result = self._connection.execute(f"""
            SELECT * FROM {table_name} WHERE DOWNLOADED=1
        """)
        downloaded = len(downloaded_result.fetchall())

        return (downloaded, total)

    def get_all_songs(self, table_name: str) -> list:
        results = self._connection.execute(f"""
            SELECT ARTIST, NAME FROM {table_name}
        """)
        return results.fetchall()

    def search_song(self, table_name: str, artist: str, name: str) -> bool:
        result = self._connection.execute(f"""
            SELECT * FROM {table_name} WHERE ARTIST=? AND NAME=?
        """, (artist, name))
        return result.fetchone() is not None

    def clear_table(self, table_name):
        self._connection.execute(f"""
            DELETE FROM {table_name};
        """)

    def commit(self):
        self._connection.commit()
