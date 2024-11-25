# backend/app/routes.py

from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import User, Character, Map, Event, Item, Inventory, Equipment, Battle, Quest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main_bp = Blueprint('main', __name__)


# 获取所有用户（仅限测试，建议在生产环境中删除或保护此路由）
@main_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
        for user in users
    ]
    return jsonify(users_data), 200


@main_bp.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    print(data)
    return jsonify({'message': 'Test success.'}), 200


# 用户注册
@main_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not username or not password or not email:
            return jsonify({'message': 'Missing required fields.'}), 400

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            return jsonify({'message': 'User already exists.'}), 409

        # new_user = User(username=username, email=email)
        # new_user.set_password(password)
        new_user = User(username=username, email=email, password=password)  # 直接存储明文密码

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully.'}), 201
    except Exception as e:
        current_app.logger.error(f"Error during registration: {e}")
        return jsonify({'message': 'Internal server error.'}), 500


# 用户登录
@main_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'message': 'Missing username or password.'}), 400

        user = User.query.filter_by(username=username).first()
        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify({'access_token': access_token}), 200
        else:
            return jsonify({'message': 'Invalid credentials.'}), 401
    except Exception as e:
        current_app.logger.error(f"Error during login: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error.'}), 500


# 获取所有角色或创建新角色
@main_bp.route('/characters', methods=['GET', 'POST'])
@jwt_required()
def manage_characters():
    try:
        current_user_id = get_jwt_identity()
        current_app.logger.debug(f"Current user ID: {current_user_id}")

        if request.method == 'GET':
            characters = Character.query.filter_by(user_id=current_user_id).all()
            characters_data = [
                {
                    'id': char.id,
                    'name': char.name,
                    'profession': char.profession,
                    'level': char.level,
                    'strength': char.strength,
                    'spirit': char.spirit,
                    'agility': char.agility,
                    'constitution': char.constitution,
                    'wisdom': char.wisdom,
                    'experience': char.experience,
                    'current_map': char.current_map,
                    'created_at': char.created_at.isoformat()
                }
                for char in characters
            ]
            return jsonify(characters_data), 200

        elif request.method == 'POST':
            data = request.get_json()
            current_app.logger.debug(f"Received data: {data}")
            name = data.get('name')
            profession = data.get('profession')

            if not name or not profession:
                current_app.logger.warning("Missing name or profession in request data.")
                return jsonify({'message': 'Missing name or profession.'}), 400

            if profession not in ['Swordmaster', 'Taoist', 'Martial Monk', 'Archer', 'Healer']:
                current_app.logger.warning(f"Invalid profession: {profession}")
                return jsonify({'message': 'Invalid profession.'}), 400

            if current_user_id is None:
                current_app.logger.warning("Invalid user ID.")
                return jsonify({'message': 'Invalid user.'}), 401

            new_character = Character(
                user_id=current_user_id,
                name=name,
                profession=profession
            )

            db.session.add(new_character)
            db.session.commit()

            current_app.logger.info(f"Character created successfully with ID: {new_character.id}")
            return jsonify({'message': 'Character created successfully.', 'character_id': new_character.id}), 201

    except Exception as e:
        current_app.logger.error(f"Error during managing characters: {e}", exc_info=True)
        return jsonify({'message': 'Internal server error.'}), 500


# 获取、更新或删除特定角色
@main_bp.route('/characters/<int:character_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def character_detail(character_id):
    current_user_id = get_jwt_identity()
    character = Character.query.filter_by(id=character_id, user_id=current_user_id).first()

    if not character:
        return jsonify({'message': 'Character not found.'}), 404

    if request.method == 'GET':
        char_data = {
            'id': character.id,
            'name': character.name,
            'profession': character.profession,
            'level': character.level,
            'strength': character.strength,
            'spirit': character.spirit,
            'agility': character.agility,
            'constitution': character.constitution,
            'wisdom': character.wisdom,
            'experience': character.experience,
            'current_map': character.current_map,
            'created_at': character.created_at.isoformat()
        }
        return jsonify(char_data), 200

    elif request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        profession = data.get('profession')

        if name:
            character.name = name
        if profession:
            if profession not in ['Swordmaster', 'Taoist', 'Martial Monk', 'Archer', 'Healer']:
                return jsonify({'message': 'Invalid profession.'}), 400
            character.profession = profession

        db.session.commit()
        return jsonify({'message': 'Character updated successfully.'}), 200

    elif request.method == 'DELETE':
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Character deleted successfully.'}), 200


# 示例：获取地图信息
@main_bp.route('/maps', methods=['GET'])
def get_maps():
    maps = Map.query.all()
    maps_data = [
        {
            'id': map_.id,
            'name': map_.name,
            'description': map_.description,
            'json_data': map_.json_data,
            'created_at': map_.created_at.isoformat()
        }
        for map_ in maps
    ]
    return jsonify(maps_data), 200


# 示例：创建地图（仅限测试，建议在生产环境中删除或保护此路由）
@main_bp.route('/maps', methods=['POST'])
def create_map():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    json_data = data.get('json_data')

    if not name:
        return jsonify({'message': 'Map name is required.'}), 400

    new_map = Map(
        name=name,
        description=description,
        json_data=json_data
    )

    db.session.add(new_map)
    db.session.commit()

    return jsonify({'message': 'Map created successfully.', 'map_id': new_map.id}), 201

# 更多路由可以根据需求添加，如事件管理、物品管理等
