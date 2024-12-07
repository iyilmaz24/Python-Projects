import sqlite3
from security import AESCipher

DB_ADDRESS = 'app.db'

def get_db_con():
    conn = sqlite3.connect(DB_ADDRESS)
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()

def create_database():
    db, cursor = get_db_con()
    
    cursor.execute(''' 
                   DROP TABLE IF EXISTS users;''')
    cursor.execute(''' 
                   DROP TABLE IF EXISTS entries;''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            UserId INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Name TEXT NOT NULL,
            Age INTEGER NOT NULL,
            PhNum TEXT NOT NULL,
            SecurityLevel INTEGER NOT NULL,
            LoginPassword TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            baking_item_name TEXT NOT NULL,
            num_excellent_votes INTEGER NOT NULL DEFAULT 0,
            num_ok_votes INTEGER NOT NULL DEFAULT 0,
            num_bad_votes INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES baking_contest_people (id)
        )
    ''')
    
    cursor.execute('''
        INSERT INTO entries (user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes)
        VALUES 
            (1, 'Ruby Brownies', 1, 2, 4),
            (2, 'Java Bars', 4, 1, 2),
            (3, 'Perl Cake', 2, 4, 2),
            (3, 'Golang Cookies', 2, 2, 1);
    ''')
        
    cursor.execute('''
                   INSERT INTO users (Username, Name, Age, PhNum, SecurityLevel, LoginPassword)
                     VALUES ('AL25', 'Alice', 25, '123-456-6789', 1, 'password1'),
                              ('BOB30', 'Bob', 30, '654-123-7890', 2, 'password2'),
                              ('CHAR35', 'Charlie', 35, '987-654-3210', 3, 'password3')
                   ''')
    
    seedUsers = cursor.execute('SELECT * FROM users').fetchall()
    cipher = AESCipher()
    
    for user in seedUsers:
        print(f"UserId: {user['UserId']}, Username: {user['Username']}, Password: {user['LoginPassword']}")
        
        encryptedUsername = cipher.encrypt(user['Username'])
        encryptedPassword = cipher.encrypt(user['LoginPassword'])
        encryptedPhNum = cipher.encrypt(user['PhNum'])
        cursor.execute('''
                       UPDATE users SET Username = ?, LoginPassword = ?, PhNum = ? WHERE UserId = ?
                       ''', (encryptedUsername, encryptedPassword, encryptedPhNum, user['UserId']))
        
    updatedUsers = cursor.execute('SELECT * FROM users')
    for user in updatedUsers:
        print(f"UserId: {user['UserId']}, Username: {user['Username']}, Password: {user['LoginPassword']}")

    db.commit()
    db.close()
    return

