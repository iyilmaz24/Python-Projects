from flask import Flask, render_template, request, redirect, url_for, session
from db import get_db_con, create_database
from form import *
import os 
from security import AESCipher
from helpers import *


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, public, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':  # display the login form
        msg = request.args.get('msg', '')
        return render_template('login.html', msg=msg)

    elif request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        encrypted_username = AesCipher.encrypt(username)
        encrypted_password = AesCipher.encrypt(password)

        db, cursor = get_db_con()
        cursor.execute('SELECT * FROM users WHERE Username = ? AND LoginPassword = ?;', (encrypted_username, encrypted_password,))
        user = cursor.fetchone()
        db.close()

        if not user:    
            return redirect(url_for('login', msg="Invalid username or password."))
        
        session['user_id'] = user['UserId']
        session['security_level'] = user['SecurityLevel']
        session['name'] = user['Name']  

        return redirect(url_for('home', msg=f"{user['name']}!"))


@app.route('/')
def home(): 
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    
    security_level = session.get('security_level')
    
    if security_level == 1:
        return redirect(url_for('home_level_1'))
    elif security_level == 2:
        return redirect(url_for('home_level_2'))
    elif security_level == 3:
        return redirect(url_for('home_level_3'))
    
    return redirect(url_for('not_found'))

@app.route('/home-level-1')
def home_level_1():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    if not session.get('security_level') == 1:
        return redirect(url_for('not_found'))
    return render_template('home1.html', msg=session.get('name'))

@app.route('/home-level-2')
def home_level_2():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    if not session.get('security_level') == 2:
        return redirect(url_for('not_found'))
    return render_template('home2.html', msg=session.get('name'))

@app.route('/home-level-3')
def home_level_3():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    if not session.get('security_level') == 3:
        return redirect(url_for('not_found'))
    return render_template('home3.html', msg=session.get('name'))


@app.route('/list-users')
def list_users(): # list all baking contest users
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    
    if not session.get('security_level') >= 2:
        return redirect(url_for('not_found'))
    
    db, cursor = get_db_con()
    
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    
    displayUsers = getDisplayUsers(AesCipher, users)
    
    db.close()
    return render_template('users_list.html', users=displayUsers)


@app.route('/list-results') 
def list_results(): # list all baking contest entries
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    
    if not session.get('security_level') == 3:
        return redirect(url_for('not_found'))
    
    db, cursor = get_db_con()
    
    cursor.execute('SELECT entry_id, user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes FROM entries')
    results = cursor.fetchall()
    
    db.close()
    return render_template('results_list.html', results=results)


@app.route('/add-user', methods=['GET', 'POST']) 
def add_user():    
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))

    if not session.get('security_level') == 3:
        return redirect(url_for('not_found'))
        
    if request.method == 'GET': # form for adding baking contest user        
        return render_template('new_user.html')
    
    elif request.method == 'POST': # adding baking contest user
        username = request.form['username'].strip()
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        phone_number = request.form['phone_number'].strip()
        security_level = request.form['security_level'].strip()
        login_password = request.form['login_password'].strip()

        errors = validate_newuser_form(username, name, age, phone_number, security_level, login_password, AesCipher.encrypt(username))
        if len(errors) > 0:
            return redirect(url_for('results', msg=("|".join(errors))))
          
        db, cursor = get_db_con()
        cursor.execute('INSERT INTO users (username, name, age, phnum, securitylevel, loginpassword) VALUES (?, ?, ?, ?, ?, ?)', 
                       (AesCipher.encrypt(username), name, int(age), AesCipher.encrypt(phone_number), int(security_level), AesCipher.encrypt(login_password)))
        
        db.commit()
        db.close()
        return redirect(url_for('results', msg=(f"{name} registered for baking contest.")))


@app.route('/add-entry', methods=['POST', 'GET'])
def add_entry():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    
    if request.method == 'GET': # form for adding baking contest entry
        return render_template('new_entry.html')
    
    baking_item_name = request.form['item_name']
    e_votes = request.form['e_votes']
    o_votes = request.form['o_votes']
    b_votes = request.form['b_votes']
    
    errors = validate_newentry_form(baking_item_name, e_votes, o_votes, b_votes)
    if len(errors) > 0:
        return redirect(url_for('results', msg=("|".join(errors))))
    
    userId = session.get('user_id')
    
    db, cursor = get_db_con()
    cursor.execute('INSERT INTO entries (user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes) VALUES (?, ?, ?, ?, ?)', 
                   (userId, baking_item_name, int(e_votes), int(o_votes), int(b_votes)))
    
    db.commit()
    db.close()
    return redirect(url_for('results', msg=(f"Entry for {baking_item_name} added.")))


@app.route('/my-entries', methods=['GET'])
def my_entries():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
        
    userId = session.get('user_id')
    db, cursor = get_db_con()
    
    cursor.execute('SELECT * FROM entries WHERE user_id = ?', (userId,))
    entries = cursor.fetchall()
    db.close()
    
    return render_template('my_entries.html', entries=entries)


@app.route('/logout')
def logout():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    session.clear()  # clear all session data
    return redirect(url_for('login'))  # redirect to the login page


@app.route('/not-found', methods=['GET'])
def not_found():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    return render_template('not_found.html')


@app.route('/results')
def results():
    if not session.get('user_id'):
        return redirect(url_for('login', msg="Please log in to view pages."))
    msg = request.args.get('msg', "Please return to home page.")
    return render_template('results.html', msg=msg)


if __name__ == '__main__':
    create_database() # create and seed database with starter data if it doesn't exist
    app.secret_key = os.urandom(12)
    AesCipher = AESCipher()
    app.run()