# from flask import Flask, render_template, request, redirect, url_for,flash
# import sqlite3

# app = Flask(__name__)
# app.secret_key = 'mithra11'

# # Create a SQLite3 database or connect to an existing one
# conn = sqlite3.connect('food_inventory.db')
# cursor = conn.cursor()

# # Create a table to store food inventory
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS inventory (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         item_name TEXT NOT NULL,
#         quantity INTEGER NOT NULL,
#         expiration_date DATE NOT NULL
#     )
# ''')
# conn.commit()
# conn.close()

# conn = sqlite3.connect('user_registration.db')
# cursor = conn.cursor()

# # Create a table to store user registration information
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         email TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')
# conn.commit()
# conn.close()


# @app.route('/',methods=['GET'])
# def index():
#     # Connect to the database and fetch the inventor
#     # conn = sqlite3.connect('food_inventory.db')
#     # cursor = conn.cursor()
#     # cursor.execute('SELECT * FROM inventory')
#     # inventory = cursor.fetchall()
#     # conn.close()
#     return render_template('index.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         # Check if the provided email and password match a user in the database
#         conn = sqlite3.connect('user_registration.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
#         user = cursor.fetchone()

#         if user:
#             flash('Login successful.', 'success')
#             return redirect(url_for('login'))
#         else:
#             flash('Login failed. Please check your email and password.', 'danger')

#     return render_template('login.html')


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         name = request.form['id']
#         email = request.form['email']
#         password = request.form['pwd']
#         confirm_password = request.form['PWD']

#         # Check if the password and confirm password match
#         if password != confirm_password:
#             flash('Password and Confirm Password do not match.', 'danger')

#         else:
#             # Insert the user into the database (you should hash the password in a real application)
#             conn = sqlite3.connect('user_registration.db')
#             cursor = conn.cursor()
#             cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
#                            (name, email, password))
#             conn.commit()
#             conn.close()

#             flash('Registration successful. You can now log in.', 'success')
#             return redirect(url_for('login'))

#     return render_template('register.html')

# @app.route('/add_item', methods=['GET', 'POST'])
# def add_item():
#     if request.method == 'POST':
#         item_name = request.form['item_name']
#         quantity = request.form['quantity']
#         expiration_date = request.form['expiration_date']

#         # Insert the new item into the database
#         conn = sqlite3.connect('food_inventory.db')
#         cursor = conn.cursor()
#         cursor.execute('INSERT INTO inventory (item_name, quantity, expiration_date) VALUES (?, ?, ?)',
#                        (item_name, quantity, expiration_date))
#         conn.commit()
#         conn.close()
#         return redirect(url_for('add_item'))
#     else:
#         # Handle the GET request to display the inventory
#         conn = sqlite3.connect('food_inventory.db')
#         cursor = conn.cursor()
#         cursor.execute('SELECT * FROM inventory')
#         inventory = cursor.fetchall()
#         conn.close()
#         return render_template('add_item.html', inventory=inventory)


# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for,flash,session,jsonify
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import warnings
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_inventory.sqlite3'  #
app.secret_key = 'mithra11'
conn = sqlite3.connect('user_registration.db')
cursor = conn.cursor()

# Create a table to store user registration information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()
conn = sqlite3.connect('food_inventory.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        expiration_date DATE NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

conn.commit()
conn.close()




@app.route('/',methods=['GET'])
def index():
    # Connect to the database and fetch the inventor
    # conn = sqlite3.connect('food_inventory.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM inventory')
    # inventory = cursor.fetchall()
    # conn.close()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the provided email and password match a user in the database
        conn = sqlite3.connect('user_registration.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()

        if user:
            # User is authenticated, set up the session
            session['logged_in'] = True
            session['user_id'] = user[0]
            flash(f'Successfully you have logged in ',category='success')

            # flash('Login successful!', 'success')
            return redirect(url_for('food_inventory'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['id']
        email = request.form['email']
        password = request.form['pwd']
        confirm_password = request.form['PWD']

        # Check if the password and confirm password match
        if password != confirm_password:
            flash('Password and Confirm Password do not match.', 'danger')
        else:
            # Check if the email already exists in the database
            conn = sqlite3.connect('user_registration.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Email already exists. Please choose a different email.', 'danger')
                return redirect(url_for('register'))
            else:
                # Insert the user into the database (you should hash the password in a real application)
                cursor.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                               (name, email, password))
                conn.commit()
                conn.close()

                flash('Registration successful. You can now log in.', 'success')
                return redirect(url_for('food_inventory'))

    return render_template('register.html')

@app.route('/food_inventory', methods=['GET', 'POST'])
def food_inventory():
    return render_template('food_inventory.html')
from datetime import datetime

# ...

@app.route('/products')
def products():
    user_id = session.get('user_id')
    conn = sqlite3.connect('food_inventory.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE user_id=?', (user_id,))
    inventory = cursor.fetchall()
    conn.close()


    # Calculate date-related statistics
    # today = datetime.now().date()
    # expiring_soon = 0
    # total_days_remaining = 0

    # for item in inventory:
    #     expiration_date = datetime.strptime(item[3], '%Y-%m-%d').date()
    #     days_until_expiration = (expiration_date - today).days

    #     if days_until_expiration >= 0:
    #         expiring_soon += 1

    #     total_days_remaining += days_until_expiration

    # if len(inventory) > 0:
    #     average_days_remaining = total_days_remaining / len(inventory)
    # else:
    #     average_days_remaining = 0

    return render_template('products.html', inventory=inventory)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        user_id = session['user_id']

        if request.method == 'POST':
            # Handle form submission for editing profile
            new_name = request.form['name']
            new_email = request.form['email']

            # Update the user's profile in the database
            conn = sqlite3.connect('user_registration.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET name = ?, email = ? WHERE id = ?', (new_name, new_email, user_id))
            conn.commit()
            conn.close()

            flash('Profile updated successfully!', 'success')

        # Retrieve user data from the database based on user_id
        conn = sqlite3.connect('user_registration.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user_name = user_data[1]
            user_email = user_data[2]

            return render_template('profile.html', user_name=user_name, user_email=user_email)

    # If the user is not logged in, redirect them to the login page
    #return redirect(url_for('login'))

@app.route('/edit_profile')
def edit_profile():
    return render_template('edit_profile.html')


@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    try:
        # Find the item in the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        item_id_to_delete = item_id # Replace with the actual item ID you want to delete
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id_to_delete,))
        conn.commit()
        conn.close()
        # Return a JSON response indicating success
        return jsonify(message='Item deleted successfully'), 204  # 204 No Content status code
    except Exception as e:
        # Handle errors and return an error response
        session.rollback()
        return jsonify(error=str(e)), 500


@app.route('/fruits_inventory',methods=['GET','POST'])
def fruits_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('fruits_inventory.html')

@app.route('/vegetable_inventory',methods=['GET','POST'])
def vegetable_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        # conn = sqlite3.connect('food_inventory.db')
        # cursor = conn.cursor()
        with sqlite3.connect('food_inventory.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
            conn.commit()
            conn.close()
        # cursor.execute('INSERT INTO inventory (item_name, quantity, expiration_date) VALUES (?, ?, ?)',
        #                (item_name, quantity, expiration_date))
        # conn.commit()
        # conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('vegetable_inventory.html')


@app.route('/meat_inventory',methods=['GET','POST'])
def meat_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('meat_inventory.html')

@app.route('/beverage_inventory',methods=['GET','POST'])
def beverage_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('beverage_inventory.html')

@app.route('/pantry_inventory',methods=['GET','POST'])
def pantry_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('pantry_inventory.html')

@app.route('/snacks_inventory',methods=['GET','POST'])
def snacks_inventory():
    if request.method == 'POST':
        user_id = session.get('user_id')
        item_name = request.form['name']
        quantity = request.form['quantity']
        expiration_date = request.form['expiration_date']

        # Insert the new item into the database
        conn = sqlite3.connect('food_inventory.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO inventory (user_id,item_name, quantity, expiration_date) VALUES (?,?, ?, ?)',
                       (user_id,item_name, quantity, expiration_date))
        conn.commit()
        conn.close()
        return redirect(url_for('food_inventory'))
    return render_template('snacks_inventory.html')

@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    return redirect(url_for('index')) 
if __name__ == '__main__':
    app.run(debug=True)
