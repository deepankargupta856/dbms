import sqlite3

def init_db():
    conn = sqlite3.connect('food_delivery.db')
    c = conn.cursor()
    
    # Create tables if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS restaurants
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  location TEXT NOT NULL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS menu_items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  restaurant_id INTEGER,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  FOREIGN KEY (restaurant_id) REFERENCES restaurants (id))''')
    
    # Clear existing data
    c.execute('DELETE FROM menu_items')
    c.execute('DELETE FROM restaurants')
    
    # Add sample restaurants
    restaurants = [
        ('Pizza Palace', 'Downtown Street, 123'),
        ('Burger Bliss', 'Main Avenue, 456'),
        ('Sushi Supreme', 'Ocean View Road, 789'),
        ('Taco Town', 'Fiesta Lane, 101'),
        ('Pasta Point', 'Roma Boulevard, 202'),
        ('Curry Corner', 'Spice Street, 303')
    ]
    
    c.executemany('INSERT INTO restaurants (name, location) VALUES (?, ?)', restaurants)
    
    # Get restaurant IDs
    c.execute('SELECT id FROM restaurants')
    restaurant_ids = [row[0] for row in c.fetchall()]
    
    # Add menu items for each restaurant
    menu_items = [
        # Pizza Palace menu
        (restaurant_ids[0], 'Margherita Pizza', 'Classic tomato and mozzarella', 12.99),
        (restaurant_ids[0], 'Pepperoni Pizza', 'Loaded with pepperoni', 14.99),
        (restaurant_ids[0], 'Vegetarian Pizza', 'Fresh garden vegetables', 13.99),
        
        # Burger Bliss menu
        (restaurant_ids[1], 'Classic Burger', 'Beef patty with lettuce and tomato', 9.99),
        (restaurant_ids[1], 'Cheese Burger', 'Classic burger with cheddar cheese', 10.99),
        (restaurant_ids[1], 'Veggie Burger', 'Plant-based patty with fresh veggies', 11.99),
        
        # Sushi Supreme menu
        (restaurant_ids[2], 'California Roll', 'Crab, avocado, and cucumber', 8.99),
        (restaurant_ids[2], 'Salmon Nigiri', 'Fresh salmon over rice', 7.99),
        (restaurant_ids[2], 'Dragon Roll', 'Eel and cucumber topped with avocado', 15.99),
        
        # Taco Town menu
        (restaurant_ids[3], 'Classic Beef Taco', 'Seasoned ground beef with lettuce and cheese', 7.99),
        (restaurant_ids[3], 'Chicken Fajita', 'Grilled chicken with peppers and onions', 8.99),
        (restaurant_ids[3], 'Veggie Burrito', 'Black beans, rice, and fresh vegetables', 9.99),
        
        # Pasta Point menu
        (restaurant_ids[4], 'Spaghetti Carbonara', 'Creamy sauce with pancetta and parmesan', 13.99),
        (restaurant_ids[4], 'Fettuccine Alfredo', 'Rich and creamy parmesan sauce', 12.99),
        (restaurant_ids[4], 'Lasagna Bolognese', 'Layers of pasta with meat sauce and cheese', 14.99),
        
        # Curry Corner menu
        (restaurant_ids[5], 'Butter Chicken', 'Tender chicken in rich tomato curry', 13.99),
        (restaurant_ids[5], 'Vegetable Biryani', 'Fragrant rice with mixed vegetables', 11.99),
        (restaurant_ids[5], 'Paneer Tikka Masala', 'Grilled cottage cheese in spiced curry', 12.99)
    ]
    
    c.executemany('''INSERT INTO menu_items 
                     (restaurant_id, name, description, price) 
                     VALUES (?, ?, ?, ?)''', menu_items)
    
    conn.commit()
    conn.close()
    print("Dummy data inserted successfully!")

if __name__ == '__main__':
    init_db() 