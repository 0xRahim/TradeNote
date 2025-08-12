import sqlite3
from flask import Flask, request, jsonify, render_template
import base64
import os # For handling potential file saving in the future, though we'll stick to base64 for now

app = Flask(__name__)
DATABASE = 'trades.db'

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Adding new columns for notes and screenshot_data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            type TEXT NOT NULL,
            trade_date TEXT NOT NULL,
            risk_amount REAL NOT NULL,
            entry_price REAL NOT NULL,
            stop_loss_price REAL NOT NULL,
            partial_close_price REAL, -- Optional, can be NULL
            take_profit_price REAL,   -- Optional, can be NULL
            won_lost_amount REAL NOT NULL,
            risk_to_reward REAL NOT NULL,
            notes TEXT,               -- New: For trade notes/comments
            screenshot_data TEXT      -- New: For base64 encoded image
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when the application starts
with app.app_context():
    init_db()

@app.route('/')
def index():
    """Serves the main HTML page."""
    # Ensure your HTML file is named index.html and is located in a 'templates' folder
    return render_template('index.html')

@app.route('/add_trade', methods=['POST'])
def add_trade():
    """Adds a new trade to the database."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Extracting all fields, including optional ones and new fields
    symbol = data.get('symbol')
    trade_type = data.get('type')
    trade_date = data.get('date')
    risk_amount = data.get('risk_amount')
    entry_price = data.get('entry_price')
    stop_loss_price = data.get('stop_loss_price')
    partial_close_price = data.get('partial_close_price')
    take_profit_price = data.get('take_profit_price')
    won_lost_amount = data.get('won_lost_amount')
    risk_to_reward = data.get('risk_to_reward')
    notes = data.get('notes')
    screenshot_data = data.get('screenshot_data')

    # Basic validation for required fields
    if not all([symbol, trade_type, trade_date, risk_amount is not None, entry_price is not None,
                stop_loss_price is not None, won_lost_amount is not None, risk_to_reward is not None]):
        return jsonify({'error': 'Missing required fields. Please ensure all fields marked with * are filled.'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO trades (symbol, type, trade_date, risk_amount, entry_price,
                                  stop_loss_price, partial_close_price, take_profit_price,
                                  won_lost_amount, risk_to_reward, notes, screenshot_data)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (symbol, trade_type, trade_date, risk_amount, entry_price,
             stop_loss_price, partial_close_price, take_profit_price,
             won_lost_amount, risk_to_reward, notes, screenshot_data)
        )
        conn.commit()
        trade_id = cursor.lastrowid
        conn.close()
        return jsonify({'message': 'Trade added successfully', 'id': trade_id}), 201
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.route('/trades', methods=['GET'])
def get_trades():
    """
    Retrieves all trades from the database, with optional filtering.
    Filters:
    - status (winner/loser): Filters by won_lost_amount (>=0 for winner, <0 for loser)
    - start_date, end_date: Filters by trade_date within a range (YYYY-MM-DD)
    - symbol: Filters by trade symbol
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM trades WHERE 1=1" # Start with a true condition
        params = []

        # Apply filters based on query parameters
        status = request.args.get('status')
        if status:
            if status == 'winner':
                query += " AND won_lost_amount >= 0"
            elif status == 'loser':
                query += " AND won_lost_amount < 0"

        start_date = request.args.get('start_date')
        if start_date:
            query += " AND trade_date >= ?"
            params.append(start_date)

        end_date = request.args.get('end_date')
        if end_date:
            query += " AND trade_date <= ?"
            params.append(end_date)

        symbol = request.args.get('symbol')
        if symbol:
            query += " AND symbol LIKE ?"
            params.append(f"%{symbol}%") # Case-insensitive search

        query += " ORDER BY trade_date DESC, id DESC" # Order by date descending

        cursor.execute(query, params)
        trades = cursor.fetchall()
        conn.close()
        trades_list = [dict(trade) for trade in trades]
        return jsonify(trades_list), 200
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.route('/trade/<int:trade_id>', methods=['GET'])
def get_trade(trade_id):
    """Retrieves a single trade by its ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades WHERE id = ?", (trade_id,))
        trade = cursor.fetchone()
        conn.close()
        if trade:
            return jsonify(dict(trade)), 200
        else:
            return jsonify({'error': 'Trade not found'}), 404
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.route('/trade/<int:trade_id>', methods=['PUT'])
def update_trade(trade_id):
    """Updates an existing trade in the database."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Extract all fields that can be updated
    symbol = data.get('symbol')
    trade_type = data.get('type')
    trade_date = data.get('date')
    risk_amount = data.get('risk_amount')
    entry_price = data.get('entry_price')
    stop_loss_price = data.get('stop_loss_price')
    partial_close_price = data.get('partial_close_price')
    take_profit_price = data.get('take_profit_price')
    won_lost_amount = data.get('won_lost_amount')
    risk_to_reward = data.get('risk_to_reward')
    notes = data.get('notes')
    screenshot_data = data.get('screenshot_data')


    # Basic validation for required fields
    if not all([symbol, trade_type, trade_date, risk_amount is not None, entry_price is not None,
                stop_loss_price is not None, won_lost_amount is not None, risk_to_reward is not None]):
        return jsonify({'error': 'Missing required fields. Please ensure all fields marked with * are filled.'}), 400


    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE trades SET symbol=?, type=?, trade_date=?, risk_amount=?, entry_price=?,
                                  stop_loss_price=?, partial_close_price=?, take_profit_price=?,
                                  won_lost_amount=?, risk_to_reward=?, notes=?, screenshot_data=?
               WHERE id = ?""",
            (symbol, trade_type, trade_date, risk_amount, entry_price,
             stop_loss_price, partial_close_price, take_profit_price,
             won_lost_amount, risk_to_reward, notes, screenshot_data, trade_id)
        )
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Trade not found or no changes made'}), 404
        return jsonify({'message': 'Trade updated successfully'}), 200
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'Internal server error: {e}'}), 500

@app.route('/trade/<int:trade_id>', methods=['DELETE'])
def delete_trade(trade_id):
    """Deletes a trade from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM trades WHERE id = ?", (trade_id,))
        conn.commit()
        conn.close()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Trade not found'}), 404
        return jsonify({'message': 'Trade deleted successfully'}), 200
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'error': f'Internal server error: {e}'}), 500


if __name__ == '__main__':
    # To run the Flask app:
    # 1. Save this code as 'app.py'.
    # 2. Create a folder named 'templates' in the same directory.
    # 3. Save the HTML code provided previously as 'index.html' inside the 'templates' folder.
    # 4. Open your terminal, navigate to the directory containing 'app.py'.
    # 5. Run the command: 'flask run'
    # The application will typically be accessible at http://127.0.0.1:5000/
    app.run(debug=True)

