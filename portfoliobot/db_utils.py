from tinydb import TinyDB, Query


db = TinyDB('templates.json')
Files = Query()


def get_file_id(filename, db_name=db):
    file_id = db_name.search(Files.filename == filename)
    return file_id


def add_file_id(filename, file_id, db_name=db):
    db_name.insert({'filename': filename, 'file_id': file_id})


def clear_database(db_name=db):
    db_name.truncate()
