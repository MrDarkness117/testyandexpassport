import sqlite3
from typing import Union
from _default_paths.paths import paths


class SQLConnection:

    def __init__(self, db: str = paths['root'] + "database.db", logger=None):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()
        self.table_name = None

    def execute(self, table_name: str = 'Users', field='username') -> None:
        query = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            """
        query += f"{field} TEXT NOT NULL"
        query += ");"
        self.cursor.execute(query)
        self.table_name = table_name
        self.connection.commit()

    def create_index(self, index_name: str, field_name, table_name="Users") -> None:
        query = f'CREATE INDEX {index_name} ON {table_name} ({field_name})'
        self.cursor.execute(query)
        self.connection.commit()

    def update_data(self, col_a: str, col_b: Union[str, int], value_a: str, value_b: Union[str, int]) -> None:
        query = f'UPDATE {self.table_name} SET {col_a} = ? WHERE {col_b} = ?'
        self.cursor.execute(query, (value_a, value_b))

    def delete_data(self, col_a, val_a) -> None:
        query = f'DELETE FROM {self.table_name} WHERE {col_a} = ?'
        self.cursor.execute(query, (val_a,))

    def fetch_data(self, data: str = "*", filters: str = ''):  # data = col_a, col_b | filters = ORDER BY col_c DESC
        query = f"SELECT {data} FROM {self.table_name} {filters}"
        self.cursor.execute(query)
        export = self.cursor.fetchall()
        return export

    def close_connection(self):
        self.connection.close()
