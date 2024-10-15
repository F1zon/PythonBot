import sqlite3 as sq

db = sq.connect('tg.db')
cur = db.cursor()

async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "chat_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS dates("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "datus TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS events("
                "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                "desc TEXT,"
                "dates INTEGER,"
                "chat_id INTEGER)")
    db.commit()