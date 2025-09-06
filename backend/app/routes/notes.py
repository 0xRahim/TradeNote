from flask import Blueprint, request, jsonify
from app.utils.auth import token_required
from app.models.note import Note
from app import db
from datetime import datetime

notes_bp = Blueprint('notes', __name__)

@notes_bp.route('/', methods=['POST'])
@token_required
def create_note(current_user):
    data = request.get_json()
    new_note = Note(title=data['title'], content=data['content'], user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created!'}), 201

@notes_bp.route('/', methods=['GET'])
@token_required
def get_notes(current_user):
    date_str = request.args.get('date')
    month_str = request.args.get('month')
    query = Note.query.filter_by(user_id=current_user.id)

    if date_str:
        try:
            note_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            query = query.filter(db.func.date(Note.created_at) == note_date)
        except ValueError:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    elif month_str:
        try:
            note_month = datetime.strptime(month_str, '%Y-%m')
            query = query.filter(db.func.year(Note.created_at) == note_month.year, db.func.month(Note.created_at) == note_month.month)
        except ValueError:
            return jsonify({'message': 'Invalid month format. Use YYYY-MM.'}), 400

    notes = query.order_by(Note.created_at.asc()).all()
    output = []
    for note in notes:
        note_data = {}
        note_data['id'] = note.id
        note_data['title'] = note.title
        note_data['content'] = note.content
        note_data['created_at'] = note.created_at.isoformat() + 'Z'
        output.append(note_data)
    return jsonify({'notes': output})

@notes_bp.route('/<int:note_id>', methods=['GET'])
@token_required
def get_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'message': 'No note found!'}), 404
    note_data = {}
    note_data['id'] = note.id
    note_data['title'] = note.title
    note_data['content'] = note.content
    note_data['created_at'] = note.created_at.isoformat() + 'Z'
    return jsonify(note_data)

@notes_bp.route('/<int:note_id>', methods=['PUT'])
@token_required
def update_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'message': 'No note found!'}), 404
    data = request.get_json()
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    db.session.commit()
    return jsonify({'message': 'Note updated!'})

@notes_bp.route('/<int:note_id>', methods=['DELETE'])
@token_required
def delete_note(current_user, note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({'message': 'No note found!'}), 404
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted!'})