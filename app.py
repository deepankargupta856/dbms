from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management

# Database initialization
def init_db():
    conn = sqlite3.connect('food_delivery.db')
    c = conn.cursor()
    
    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    
    # Create Restaurants table
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  location TEXT NOT NULL)''')
    
    # Create MenuItems table
    c.execute('''CREATE TABLE IF NOT EXISTS menu_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  restaurant_id INTEGER,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  FOREIGN KEY (restaurant_id) REFERENCES restaurants (id))''')
    
    # Create Cart table
    c.execute('''CREATE TABLE IF NOT EXISTS cart
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  item_id INTEGER,
                  quantity INTEGER NOT NULL,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (item_id) REFERENCES menu_items (id))''')
    
    # Create Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  total_price REAL NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect('food_delivery.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                        (name, email, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists!', 'error')
        finally:
            conn.close()
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/restaurants')
def restaurants():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    restaurants = conn.execute('SELECT * FROM restaurants').fetchall()
    conn.close()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/menu/<int:restaurant_id>')
def menu(restaurant_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    restaurant = conn.execute('SELECT * FROM restaurants WHERE id = ?', (restaurant_id,)).fetchone()
    menu_items = conn.execute('SELECT * FROM menu_items WHERE restaurant_id = ?', (restaurant_id,)).fetchall()
    conn.close()
    
    return render_template('menu.html', restaurant=restaurant, menu_items=menu_items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    item_id = request.form.get('item_id')
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db()
    # Check if item already in cart
    existing_item = conn.execute('SELECT * FROM cart WHERE user_id = ? AND item_id = ?',
                               (session['user_id'], item_id)).fetchone()
    
    if existing_item:
        conn.execute('UPDATE cart SET quantity = quantity + ? WHERE user_id = ? AND item_id = ?',
                    (quantity, session['user_id'], item_id))
    else:
        conn.execute('INSERT INTO cart (user_id, item_id, quantity) VALUES (?, ?, ?)',
                    (session['user_id'], item_id, quantity))
    
    conn.commit()
    conn.close()
    
    flash('Item added to cart!', 'success')
    return redirect(request.referrer)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cart_items = conn.execute('''
        SELECT cart.id, menu_items.name, menu_items.price, cart.quantity,
               menu_items.price * cart.quantity as subtotal
        FROM cart
        JOIN menu_items ON cart.item_id = menu_items.id
        WHERE cart.user_id = ?
    ''', (session['user_id'],)).fetchall()
    
    total = sum(item['subtotal'] for item in cart_items)
    conn.close()
    
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/update_cart', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_id = request.form.get('cart_id')
    quantity = int(request.form.get('quantity'))
    
    conn = get_db()
    if quantity > 0:
        conn.execute('UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?',
                    (quantity, cart_id, session['user_id']))
    else:
        conn.execute('DELETE FROM cart WHERE id = ? AND user_id = ?',
                    (cart_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    flash('Cart updated!', 'success')
    return redirect(url_for('cart'))

@app.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    # Calculate total price
    cart_items = conn.execute('''
        SELECT menu_items.price * cart.quantity as subtotal
        FROM cart
        JOIN menu_items ON cart.item_id = menu_items.id
        WHERE cart.user_id = ?
    ''', (session['user_id'],)).fetchall()
    
    total_price = sum(item['subtotal'] for item in cart_items)
    
    if total_price > 0:
        # Create order
        conn.execute('INSERT INTO orders (user_id, total_price) VALUES (?, ?)',
                    (session['user_id'], total_price))
        # Clear cart
        conn.execute('DELETE FROM cart WHERE user_id = ?', (session['user_id'],))
        conn.commit()
        flash('Order placed successfully!', 'success')
    else:
        flash('Your cart is empty!', 'error')
    
    conn.close()
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    orders = conn.execute('''
        SELECT id, total_price, timestamp
        FROM orders
        WHERE user_id = ?
        ORDER BY timestamp DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('orders.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True) 
    