"""
HTTP API for controlling the trading engine (paper trading simulation)
"""
from flask import Flask, request, jsonify
import threading
import logging
import asyncio
from trading_engine.analysis import trade_logger

app = Flask(__name__)
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Shared references (set by main)
bot_instance = None
virtual_account = None

# Debug: print all routes on startup
@app.route('/_routes', methods=['GET'])
def list_routes():
    import urllib.parse
    routes = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        routes.append(f"{rule.endpoint} [{methods}] {rule}")
    return jsonify({'routes': routes})

@app.route('/command', methods=['POST'])
def command():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    action = data.get('action')
    if action == 'reset_balance':
        new_balance = data.get('balance', 1000.0)
        if virtual_account:
            virtual_account.reset_balance(new_balance)
            trade_logger.log_balance(new_balance)
            return jsonify({'status': 'ok', 'balance': new_balance})
        else:
            return jsonify({'error': 'Virtual account not available'}), 500
    
    elif action == 'set_balance':
        new_balance = data.get('balance')
        if new_balance is None:
            return jsonify({'error': 'Missing balance parameter'}), 400
        if virtual_account:
            virtual_account.reset_balance(new_balance)
            trade_logger.log_balance(new_balance)
            return jsonify({'status': 'ok', 'balance': new_balance})
        else:
            return jsonify({'error': 'Virtual account not available'}), 500
    
    else:
        return jsonify({'error': 'Unknown action'}), 400

@app.route('/positions', methods=['GET'])
def get_positions():
    if not virtual_account:
        return jsonify({'error': 'Virtual account not available'}), 500
    positions = virtual_account.get_positions()
    # Convert to serializable format
    result = []
    for symbol, pos in positions.items():
        result.append({
            'symbol': symbol,
            'side': pos.side,
            'entry_price': pos.entry_price,
            'size': pos.size,
            'leverage': pos.leverage,
            'pnl': pos.pnl
        })
    return jsonify({'positions': result})

@app.route('/balance', methods=['GET'])
def get_balance():
    if not virtual_account:
        return jsonify({'error': 'Virtual account not available'}), 500
    return jsonify({'balance': virtual_account.get_balance()})

@app.route('/reset', methods=['POST'])
def reset():
    data = request.get_json() or {}
    new_balance = data.get('balance', 1000.0)
    if bot_instance is None:
        return jsonify({'error': 'Bot instance not available'}), 500
    # Schedule the reset coroutine in the bot's event loop
    if hasattr(bot_instance, 'loop'):
        future = asyncio.run_coroutine_threadsafe(
            bot_instance.close_all_positions(),
            bot_instance.loop
        )
        # Wait for result (with timeout)
        try:
            future.result(timeout=5)
        except Exception as e:
            return jsonify({'error': f'Failed to close positions: {e}'}), 500
    else:
        return jsonify({'error': 'Bot loop not available'}), 500
    # Reset virtual account balance
    if virtual_account:
        virtual_account.reset_balance(new_balance)
    else:
        return jsonify({'error': 'Virtual account not available'}), 500
    return jsonify({'status': 'ok', 'balance': new_balance})

@app.route('/config', methods=['POST'])
def update_config():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    if bot_instance is None:
        return jsonify({'error': 'Bot instance not available'}), 500
    # Update bot's config dictionary
    for key, value in data.items():
        bot_instance.config[key] = value
        trade_logger.log_config_change(key, value)
    return jsonify({'status': 'ok', 'updated': list(data.keys())})

def run_api(host='0.0.0.0', port=5000):
    """Run Flask API server"""
    app.run(host=host, port=port, debug=False, use_reloader=False)

def start_api_thread(host='0.0.0.0', port=5000):
    """Start API server in a background thread"""
    thread = threading.Thread(target=run_api, args=(host, port), daemon=True)
    thread.start()
    return thread