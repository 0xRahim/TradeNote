from flask import Blueprint, request, jsonify, current_app, send_from_directory
from sqlalchemy import extract
from app.utils.auth import token_required
from app.models.trade import Trade
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json

trades_bp = Blueprint('trades', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@trades_bp.route('/', methods=['POST'])
@token_required
def create_trade(current_user):
    data = request.form
    filename = None
    if 'screenshot' in request.files:
        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    new_trade = Trade(
        ticker=data['ticker'],
        result=data['result'],
        total_pnl=float(data['total_pnl']),
        entry_datetime=datetime.fromisoformat(data['entry_datetime'].replace('Z', '+00:00')),
        exit_datetime=datetime.fromisoformat(data['exit_datetime'].replace('Z', '+00:00')),
        risk_reward=float(data['risk_reward']),
        position=data['position'],
        stoploss_pips=int(data['stoploss_pips']),
        trade_range=int(data['range']),
        result_type=data['result_type'],
        entry_model=data['entry_model'],
        trade_model=data['trade_model'],
        setup_type=data['setup_type'],
        confluences=json.loads(data['confluences']),
        trade_note=data.get('trade_note'),
        roadmap=data.get('roadmap'),
        screenshot_filename=filename,
        user_id=current_user.id
    )
    db.session.add(new_trade)
    db.session.commit()
    return jsonify({'message': 'Trade created!'}), 201

@trades_bp.route('/', methods=['GET'])
@token_required
def get_trades(current_user):
    date_str = request.args.get('date')
    month_str = request.args.get('month')
    query = Trade.query.filter_by(user_id=current_user.id)

    if date_str:
        try:
            trade_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Trade.entry_datetime) == trade_date)
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    elif month_str:
        try:
            trade_month = datetime.strptime(month_str, '%Y-%m')
            query = query.filter(extract('year', Trade.entry_datetime) == trade_month.year, extract('month', Trade.entry_datetime) == trade_month.month)
        except ValueError:
            return jsonify({'message': 'Invalid month format. Use YYYY-MM.'}), 400


    trades = query.order_by(Trade.entry_datetime.asc()).all()
    output = []
    for trade in trades:
        trade_data = {
            'id': trade.id,
            'ticker': trade.ticker,
            'result': trade.result,
            'total_pnl': trade.total_pnl,
            'entry_datetime': trade.entry_datetime.isoformat() + 'Z',
            'exit_datetime': trade.exit_datetime.isoformat() + 'Z',
            'risk_reward': trade.risk_reward,
            'position': trade.position,
            'stoploss_pips': trade.stoploss_pips,
            'trade_range': trade.trade_range,
            'result_type': trade.result_type,
            'entry_model': trade.entry_model,
            'trade_model': trade.trade_model,
            'setup_type': trade.setup_type,
            'confluences': trade.confluences,
            'trade_note': trade.trade_note,
            'roadmap': trade.roadmap,
            'screenshot_filename': trade.screenshot_filename
        }
        output.append(trade_data)
    return jsonify({'trades': output})

@trades_bp.route('/<int:trade_id>', methods=['GET'])
@token_required
def get_trade(current_user, trade_id):
    trade = Trade.query.filter_by(id=trade_id, user_id=current_user.id).first()
    if not trade:
        return jsonify({'message': 'No trade found!'}), 404
    trade_data = {
        'id': trade.id,
        'ticker': trade.ticker,
        'result': trade.result,
        'total_pnl': trade.total_pnl,
        'entry_datetime': trade.entry_datetime.isoformat() + 'Z',
        'exit_datetime': trade.exit_datetime.isoformat() + 'Z',
        'risk_reward': trade.risk_reward,
        'position': trade.position,
        'stoploss_pips': trade.stoploss_pips,
        'trade_range': trade.trade_range,
        'result_type': trade.result_type,
        'entry_model': trade.entry_model,
        'trade_model': trade.trade_model,
        'setup_type': trade.setup_type,
        'confluences': trade.confluences,
        'trade_note': trade.trade_note,
        'roadmap': trade.roadmap,
        'screenshot_filename': trade.screenshot_filename
    }
    return jsonify(trade_data)

@trades_bp.route('/<int:trade_id>', methods=['PUT'])
@token_required
def update_trade(current_user, trade_id):
    trade = Trade.query.filter_by(id=trade_id, user_id=current_user.id).first()
    if not trade:
        return jsonify({'message': 'No trade found!'}), 404
    data = request.form
    
    trade.ticker = data.get('ticker', trade.ticker)
    trade.result = data.get('result', trade.result)
    trade.total_pnl = float(data.get('total_pnl', trade.total_pnl))
    if 'entry_datetime' in data:
        trade.entry_datetime = datetime.fromisoformat(data['entry_datetime'].replace('Z', '+00:00'))
    if 'exit_datetime' in data:
        trade.exit_datetime = datetime.fromisoformat(data['exit_datetime'].replace('Z', '+00:00'))
    trade.risk_reward = float(data.get('risk_reward', trade.risk_reward))
    trade.position = data.get('position', trade.position)
    trade.stoploss_pips = int(data.get('stoploss_pips', trade.stoploss_pips))
    trade.trade_range = int(data.get('range', trade.trade_range))
    trade.result_type = data.get('result_type', trade.result_type)
    trade.entry_model = data.get('entry_model', trade.entry_model)
    trade.trade_model = data.get('trade_model', trade.trade_model)
    trade.setup_type = data.get('setup_type', trade.setup_type)
    if 'confluences' in data:
        trade.confluences = json.loads(data['confluences'])
    trade.trade_note = data.get('trade_note', trade.trade_note)
    trade.roadmap = data.get('roadmap', trade.roadmap)

    if 'screenshot' in request.files:
        file = request.files['screenshot']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if trade.screenshot_filename:
                try:
                    os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], trade.screenshot_filename))
                except FileNotFoundError:
                    pass # Ignore if file does not exist
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            trade.screenshot_filename = filename

    db.session.commit()
    return jsonify({'message': 'Trade updated!'})

@trades_bp.route('/<int:trade_id>', methods=['DELETE'])
@token_required
def delete_trade(current_user, trade_id):
    trade = Trade.query.filter_by(id=trade_id, user_id=current_user.id).first()
    if not trade:
        return jsonify({'message': 'No trade found!'}), 404
    if trade.screenshot_filename:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], trade.screenshot_filename))
        except FileNotFoundError:
            pass # Ignore if file does not exist
    db.session.delete(trade)
    db.session.commit()
    return jsonify({'message': 'Trade deleted!'})

@trades_bp.route('/screenshots/<path:filename>', methods=['GET'])
@token_required
def get_screenshot(current_user, filename):
    trade = Trade.query.filter_by(screenshot_filename=filename, user_id=current_user.id).first()
    if not trade:
        return jsonify({'message': 'Not authorized to access this screenshot or screenshot not found'}), 403
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)