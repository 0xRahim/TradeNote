from flask import Blueprint, request, jsonify
from app.utils.auth import token_required
from app.models.playbook import Playbook
from app import db
import uuid

playbooks_bp = Blueprint('playbooks', __name__)

@playbooks_bp.route('/', methods=['POST'])
@token_required
def create_playbook(current_user):
    data = request.get_json()
    playbook_id = f"pb_{str(uuid.uuid4())[:8]}"
    
    new_playbook = Playbook(
        playbook_id=playbook_id,
        title=data['title'],
        entry_model=data['entry_model'],
        trade_model=data['trade_model'],
        setup_grade=data['setup_grade'],
        confluences=data.get('confluences'),
        rules=data.get('rules'),
        confirmations=data.get('confirmations'),
        invalidations=data.get('invalidations'),
        roadmap=data.get('roadmap'),
        tags=data.get('tags'),
        user_id=current_user.id
    )
    db.session.add(new_playbook)
    db.session.commit()
    return jsonify({'message': 'Playbook created!', 'playbook_id': playbook_id}), 201

@playbooks_bp.route('/', methods=['GET'])
@token_required
def get_playbooks(current_user):
    playbooks = Playbook.query.filter_by(user_id=current_user.id).all()
    output = []
    for playbook in playbooks:
        playbook_data = {
            'playbook_id': playbook.playbook_id,
            'title': playbook.title,
            'entry_model': playbook.entry_model,
            'trade_model': playbook.trade_model,
            'setup_grade': playbook.setup_grade,
            'created_at': playbook.created_at.isoformat() + 'Z',
            'updated_at': playbook.updated_at.isoformat() + 'Z'
        }
        output.append(playbook_data)
    return jsonify({'playbooks': output})

@playbooks_bp.route('/<playbook_id>', methods=['GET'])
@token_required
def get_playbook(current_user, playbook_id):
    playbook = Playbook.query.filter_by(playbook_id=playbook_id, user_id=current_user.id).first()
    if not playbook:
        return jsonify({'message': 'No playbook found!'}), 404
    playbook_data = {
        'playbook_id': playbook.playbook_id,
        'title': playbook.title,
        'entry_model': playbook.entry_model,
        'trade_model': playbook.trade_model,
        'setup_grade': playbook.setup_grade,
        'confluences': playbook.confluences,
        'rules': playbook.rules,
        'confirmations': playbook.confirmations,
        'invalidations': playbook.invalidations,
        'roadmap': playbook.roadmap,
        'tags': playbook.tags,
        'created_at': playbook.created_at.isoformat() + 'Z',
        'updated_at': playbook.updated_at.isoformat() + 'Z'
    }
    return jsonify(playbook_data)

@playbooks_bp.route('/<playbook_id>', methods=['PUT'])
@token_required
def update_playbook(current_user, playbook_id):
    playbook = Playbook.query.filter_by(playbook_id=playbook_id, user_id=current_user.id).first()
    if not playbook:
        return jsonify({'message': 'No playbook found!'}), 404
    data = request.get_json()
    
    playbook.title = data.get('title', playbook.title)
    playbook.entry_model = data.get('entry_model', playbook.entry_model)
    playbook.trade_model = data.get('trade_model', playbook.trade_model)
    playbook.setup_grade = data.get('setup_grade', playbook.setup_grade)
    playbook.confluences = data.get('confluences', playbook.confluences)
    playbook.rules = data.get('rules', playbook.rules)
    playbook.confirmations = data.get('confirmations', playbook.confirmations)
    playbook.invalidations = data.get('invalidations', playbook.invalidations)
    playbook.roadmap = data.get('roadmap', playbook.roadmap)
    playbook.tags = data.get('tags', playbook.tags)

    db.session.commit()
    return jsonify({'message': 'Playbook updated!'})

@playbooks_bp.route('/<playbook_id>', methods=['DELETE'])
@token_required
def delete_playbook(current_user, playbook_id):
    playbook = Playbook.query.filter_by(playbook_id=playbook_id, user_id=current_user.id).first()
    if not playbook:
        return jsonify({'message': 'No playbook found!'}), 404
    db.session.delete(playbook)
    db.session.commit()
    return jsonify({'message': 'Playbook deleted!'})
