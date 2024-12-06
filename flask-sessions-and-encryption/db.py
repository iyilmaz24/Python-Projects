import sqlite3

DB_ADDRESS = 'app.db'

def get_db_con():
    conn = sqlite3.connect(DB_ADDRESS)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def create_database():
    db, cursor = get_db_con()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS baking_contest_people (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone_number TEXT NOT NULL,
            security_level INTEGER NOT NULL,
            login_password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS baking_contest_entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            baking_item_name TEXT NOT NULL,
            num_excellent_votes INTEGER NOT NULL DEFAULT 0,
            num_ok_votes INTEGER NOT NULL DEFAULT 0,
            num_bad_votes INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES baking_contest_people (id)
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) AS count FROM baking_contest_entries')
    result = cursor.fetchone()
    
    if result['count'] == 0: # if no entries exist - add starter data
        cursor.execute('''
            INSERT INTO baking_contest_entries (user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes)
            VALUES 
                (1, 'Ruby Brownies', 1, 2, 4),
                (2, 'Java Bars', 4, 1, 2),
                (3, 'C# Cake', 2, 4, 2),
                (4, 'Golang Cookies', 2, 2, 1);
        ''')
    
    db.commit()
    db.close()
    return