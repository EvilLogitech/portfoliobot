from tinydb import TinyDB, Query
from pathlib import Path


DB_DIR = Path(__file__).resolve().parent.parent
db_name = DB_DIR / 'file_ids.json'
db = TinyDB(db_name)
Files = Query()


def get_file_id(filename, db_name=db):
    table = db_name.table('_default')
    file_id = table.search(Files.filename == filename)
    if file_id:
        return file_id[-1].get('file_id')


def add_file_id(filename, file_id, db_name=db):
    table = db_name.table('_default')
    table.insert({'filename': filename, 'file_id': file_id})


def add_user(user, db_name=db):
    table = db_name.table('subscribers')
    user_dict = {
        'user_id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
    table.upsert(user_dict, Files.username == user.username)


def clear_database(db_name=db):
    db_name.truncate()
