from tinydb import TinyDB, Query
from pathlib import Path


DB_DIR = Path(__file__).resolve().parent.parent
db_name = DB_DIR / 'file_ids.json'
db = TinyDB(db_name)
Files = Query()


def get_file_id(filename, db_name=db):
    file_id = db_name.search(Files.filename == filename)
    if file_id:
        return file_id[-1].get('file_id')


def add_file_id(filename, file_id, db_name=db):
    db_name.insert({'filename': filename, 'file_id': file_id})


def clear_database(db_name=db):
    db_name.truncate()
