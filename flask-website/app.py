from flask import Flask, render_template, request, redirect, url_for
from db import get_db_con, create_database
from form import validate_form


app = Flask(__name__)
@app.route('/')
def home(): 
    return render_template('home.tmpl')


@app.route('/list-users')
def list_users(): # list all baking contest users
    db, cursor = get_db_con()
    
    cursor.execute('SELECT * FROM baking_contest_people')
    users = cursor.fetchall()
    
    db.close()
    return render_template('users_list.tmpl', users=users)


@app.route('/list-results') 
def list_results(): # list all baking contest entries
    db, cursor = get_db_con()
    
    cursor.execute('SELECT entry_id, user_id, baking_item_name, num_excellent_votes, num_ok_votes, num_bad_votes FROM baking_contest_entries')
    results = cursor.fetchall()
    
    db.close()
    return render_template('results_list.tmpl', results=results)


@app.route('/results')
def results():
    msg = request.args.get('msg', "Please return to home page.")
    return render_template('results.tmpl', msg=msg)


@app.route('/add-user', methods=['GET', 'POST']) 
def add_user():
    if request.method == 'GET': # form for adding baking contest user
        return render_template('new_user.tmpl')
    
    elif request.method == 'POST': # adding baking contest user
        name = request.form['name'].strip()
        age = request.form['age'].strip()
        phone_number = request.form['phone_number'].strip()
        security_level = request.form['security_level'].strip()
        login_password = request.form['login_password'].strip()

        errors = validate_form(name, age, phone_number, security_level, login_password)
        if len(errors) > 0:
            return redirect(url_for('results', msg=("<br />".join(errors))))
        
        db, cursor = get_db_con()
        cursor.execute('INSERT INTO baking_contest_people (name, age, phone_number, security_level, login_password) VALUES (?, ?, ?, ?, ?)', 
                       (name, int(age), phone_number, int(security_level), login_password))
        db.commit()
        db.close()
        
        return redirect(url_for('results', msg=(f"{name} registered for baking contest.")))


if __name__ == '__main__':
    create_database() # create and seed database with starter data if it doesn't exist
    app.run()
