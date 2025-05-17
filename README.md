# Food Delivery System

A Flask-based web application for a food delivery system with user authentication, restaurant listings, menu management, shopping cart, and order tracking.

## Features

- User registration and authentication
- Browse restaurants and their menus
- Add items to cart
- Update cart quantities
- Place orders
- View order history
- Responsive design using Bootstrap 5

## Requirements

- Python 3.7+
- Flask 3.0.2
- Werkzeug 3.0.1

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd food_delivery_system
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Database

The application uses SQLite as the database. The database file (`food_delivery.db`) will be created automatically when you run the application for the first time.

## Project Structure

```
food_delivery_system/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── food_delivery.db   # SQLite database (created automatically)
├── README.md          # This file
├── static/            # Static files (if any)
└── templates/         # HTML templates
    ├── layout.html    # Base template
    ├── index.html     # Homepage
    ├── signup.html    # User registration
    ├── login.html     # User login
    ├── restaurants.html # Restaurant listing
    ├── menu.html      # Restaurant menu
    ├── cart.html      # Shopping cart
    └── orders.html    # Order history
```

## Security Notes

- Passwords are hashed using Werkzeug's security functions
- Session management is handled by Flask's session
- SQL injection is prevented by using parameterized queries
- CSRF protection is provided by Flask's built-in features

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 