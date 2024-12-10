# backend/app/routes/characters.py

from flask import Blueprint, request, jsonify
from ..models import db, User, Character

characters_bp = Blueprint('characters', __name__)


@characters_bp.route('/', methods=['POST'])
def create_character():
    data = request.get_json()
    user_id = data.get('user_id')  # 假设前端传递 user_id
    name = data.get('name')
    profession = data.get('profession')

    if not user_id or not name or not profession:
        return jsonify({'message': '缺少必要参数'}), 400

    if profession not in ['剑侠', '武者', '医士', '刺客', '道士']:
        return jsonify({'message': '无效的职业'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': '用户不存在'}), 404

    new_character = Character(
        user_id=user_id,
        name=name,
        profession=profession
    )
    db.session.add(new_character)
    db.session.commit()

    return jsonify({'message': '角色创建成功', 'character_id': new_character.id}), 201


@characters_bp.route('/', methods=['GET'])
def get_characters():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'message': '缺少 user_id 参数'}), 400

    characters = Character.query.filter_by(user_id=user_id).all()

    if not characters:
        return jsonify({'message': '未找到角色'}), 404

    characters_data = []
    for char in characters:
        characters_data.append({
            'id': char.id,
            'name': char.name,
            'profession': char.profession,
            'level': char.level,
            'experience': char.experience,
            'health': char.health,
            'attack': char.attack,
            'defense': char.defense,
            'mana': char.mana,
            'inventory_capacity': char.inventory_capacity,
            'created_at': char.created_at
        })

    return jsonify({'characters': characters_data}), 200


@characters_bp.route('/<int:character_id>', methods=['GET'])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    character_data = {
        'id': character.id,
        'user_id': character.user_id,
        'name': character.name,
        'profession': character.profession,
        'level': character.level,
        'experience': character.experience,
        'health': character.health,
        'attack': character.attack,
        'defense': character.defense,
        'mana': character.mana,
        'inventory_capacity': character.inventory_capacity,
        'created_at': character.created_at
    }

    return jsonify({'character': character_data}), 200


@characters_bp.route('/<int:character_id>', methods=['PUT'])
def update_character(character_id):
    data = request.get_json()
    name = data.get('name')
    profession = data.get('profession')

    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    if name:
        character.name = name
    if profession:
        if profession not in ['剑侠', '武者', '医士', '刺客', '道士']:
            return jsonify({'message': '无效的职业'}), 400
        character.profession = profession

    db.session.commit()

    return jsonify({'message': '角色信息已更新'}), 200


@characters_bp.route('/<int:character_id>', methods=['DELETE'])
def delete_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    db.session.delete(character)
    db.session.commit()

    return jsonify({'message': '角色已删除'}), 200
