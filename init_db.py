import sqlite3

def init_sample_data():
    conn = sqlite3.connect('food_delivery.db')
    c = conn.cursor()
    
    # Add sample restaurants
    restaurants = [
        ('Pizza Palace', 'Downtown Street, 123'),
        ('Burger Bliss', 'Main Avenue, 456'),
        ('Sushi Supreme', 'Ocean View Road, 789')
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
        (restaurant_ids[2], 'Salmon rolls', 'Fresh salmon over rice', 7.99),
        (restaurant_ids[2], 'Dragon Roll', 'Eel and cucumber topped with avocado', 15.99)
    ]
    
    c.executemany('''INSERT INTO menu_items 
                     (restaurant_id, name, description, price) 
                     VALUES (?, ?, ?, ?)''', menu_items)
    
    conn.commit()
    conn.close()
    print("Sample data has been initialized successfully!")

if __name__ == '__main__':
    init_sample_data() 