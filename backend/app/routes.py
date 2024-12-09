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
        level = data.get('level')
        strength = data.get('strength')
        spirit = data.get('spirit')
        agility = data.get('agility')
        constitution = data.get('constitution')
        wisdom = data.get('wisdom')
        experience = data.get('experience')

        if name:
            character.name = name
        if profession:
            if profession not in ['Swordmaster', 'Taoist', 'Martial Monk', 'Archer', 'Healer']:
                return jsonify({'message': 'Invalid profession.'}), 400
            character.profession = profession
        if level:
            character.level = level
        if strength:
            character.strength = strength
        if spirit:
            character.spirit = spirit
        if agility:
            character.agility = agility
        if constitution:
            character.constitution = constitution
        if wisdom:
            character.wisdom = wisdom
        if experience:
            character.experience = experience

        db.session.commit()
        return jsonify({'message': 'Character updated successfully.'}), 200

    elif request.method == 'DELETE':
        db.session.delete(character)
        db.session.commit()
        return jsonify({'message': 'Character deleted successfully.'}), 200


# 示例：获取地图信息
@main_bp.route('/maps', methods=['GET', 'POST'])
@jwt_required(optional=True)  # 允许未认证用户查看地图
def manage_maps():
    # 获取所有地图
    if request.method == 'GET':
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

    # 创建新地图
    elif request.method == 'POST':
        # 仅管理员或特定角色可以创建地图
        current_user_id = get_jwt_identity()
        # 假设有角色验证逻辑，这里简化
        # 例如，检查用户是否有创建地图的权限
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


# 获取特定地图
@main_bp.route('/maps/<int:map_id>', methods=['GET'])
def get_map(map_id):
    map_ = Map.query.get(map_id)
    if not map_:
        return jsonify({'message': 'Map not found.'}), 404

    map_data = {
        'id': map_.id,
        'name': map_.name,
        'description': map_.description,
        'json_data': map_.json_data,
        'created_at': map_.created_at.isoformat()
    }
    return jsonify(map_data), 200


# 战斗系统 - 触发战斗
@main_bp.route('/battles', methods=['POST'])
@jwt_required()
def initiate_battle():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    character_id = data.get('character_id')
    event_id = data.get('event_id')

    # 获取角色和事件
    character = Character.query.filter_by(id=character_id, user_id=current_user_id).first()
    event = Event.query.filter_by(id=event_id).first()

    if not character:
        return jsonify({'message': '角色未找到。'}), 404
    if not event:
        return jsonify({'message': '事件未找到。'}), 404
    if event.category != 'Combat':
        return jsonify({'message': '事件不是战斗类型。'}), 400

    # 战斗逻辑
    import random
    outcome = random.choice(['Victory', 'Defeat'])

    if outcome == 'Victory':
        experience_gained = 50
        # 随机掉落物品
        items_dropped = []
        if random.random() < 0.5:  # 50% 概率掉落物品
            dropped_item = Item.query.order_by(db.func.random()).first()
            if dropped_item:
                items_dropped.append({'item_id': dropped_item.id, 'quantity': 1})
                # 更新用户的物品库存
                inventory = Inventory.query.filter_by(user_id=current_user_id, item_id=dropped_item.id).first()
                if inventory:
                    inventory.quantity += 1
                else:
                    new_inventory = Inventory(user_id=current_user_id, item_id=dropped_item.id, quantity=1)
                    db.session.add(new_inventory)
        character.experience += experience_gained
        db.session.commit()
    else:
        experience_gained = 0
        items_dropped = None

    # 记录战斗
    battle = Battle(
        character_id=character.id,
        event_id=event.id,
        result=outcome,
        experience_gained=experience_gained,
        items_dropped=items_dropped
    )
    db.session.add(battle)
    db.session.commit()

    battle_data = {
        'id': battle.id,
        'character_id': battle.character_id,
        'event_id': battle.event_id,
        'result': battle.result,
        'experience_gained': battle.experience_gained,
        'items_dropped': battle.items_dropped,
        'created_at': battle.created_at.isoformat()
    }

    return jsonify({'battle': battle_data}), 201


# 查询事件
@main_bp.route('/events', methods=['GET'])
@jwt_required(optional=True)  # 允许未认证用户查看事件
def get_events():
    events = Event.query.all()
    events_data = [
        {
            'id': event.id,
            'description': event.description,
            'map_id': event.map_id,
            'conditions': event.conditions,
            'results': event.results,
            'created_at': event.created_at.isoformat()
        }
        for event in events
    ]
    return jsonify(events_data), 200


# 后端实现战斗事件
@main_bp.route('/events/combat', methods=['GET'])
@jwt_required(optional=True)  # 允许未认证用户查看事件
def get_combat_events():
    # 获取所有战斗类型的事件
    events = Event.query.filter_by(event_type='Combat').all()
    events_data = [
        {
            'id': event.id,
            'description': event.description,
            'map_id': event.map_id,
            'conditions': event.conditions,
            'results': event.results,
            'created_at': event.created_at.isoformat()
        }
        for event in events
    ]
    return jsonify(events_data), 200


# 物品管理 - 获取特定物品

@main_bp.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found.'}), 404

    item_data = {
        'id': item.id,
        'name': item.name,
        'type': item.type,
        'attributes': item.attributes,
        'description': item.description,
        'created_at': item.created_at.isoformat()
    }
    return jsonify(item_data), 200


# 物品管理 - 获取所有物品
@main_bp.route('/items', methods=['GET', 'POST'])
@jwt_required(optional=True)  # 允许未认证用户查看物品
def manage_items():
    if request.method == 'GET':
        items = Item.query.all()
        items_data = [
            {
                'id': item.id,
                'name': item.name,
                'type': item.type,
                'attributes': item.attributes,
                'description': item.description,
                'created_at': item.created_at.isoformat()
            }
            for item in items
        ]
        return jsonify(items_data), 200

    elif request.method == 'POST':
        # 仅管理员或特定角色可以创建物品
        current_user_id = get_jwt_identity()
        # 假设有角色验证逻辑，这里简化
        data = request.get_json()
        name = data.get('name')
        type_ = data.get('type')
        attributes = data.get('attributes')
        description = data.get('description')

        if not name or not type_:
            return jsonify({'message': 'Name and type are required.'}), 400

        if type_ not in ['Weapon', 'Armor', 'Accessory', 'Consumable', 'Special']:
            return jsonify({'message': 'Invalid item type.'}), 400

        new_item = Item(
            name=name,
            type=type_,
            attributes=attributes,
            description=description
        )

        db.session.add(new_item)
        db.session.commit()

        return jsonify({'message': 'Item created successfully.', 'item_id': new_item.id}), 201


# 创建任务
@main_bp.route('/quests', methods=['POST'])
@jwt_required()
def create_quest():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    character_id = data.get('character_id')
    event_id = data.get('event_id')

    # 获取角色和事件
    character = Character.query.filter_by(id=character_id, user_id=current_user_id).first()
    event = Event.query.filter_by(id=event_id).first()

    if not character:
        return jsonify({'message': 'Character not found.'}), 404
    if not event:
        return jsonify({'message': 'Event not found.'}), 404

    # 创建任务
    quest = Quest(
        character_id=character.id,
        event_id=event.id,
        status='Active'
    )
    db.session.add(quest)
    db.session.commit()

    quest_data = {
        'id': quest.id,
        'character_id': quest.character_id,
        'event_id': quest.event_id,
        'status': quest.status,
        'created_at': quest.created_at.isoformat(),
        'updated_at': quest.updated_at.isoformat()
    }

    return jsonify(quest_data), 201


# 获取所有的角色任务
@main_bp.route('/characters/quests', methods=['GET'])
@jwt_required()
def get_all_quests():
    # 直接查询quets表中的所有记录
    quests = Quest.query.all()
    quests_data = [
        {
            'id': quest.id,
            'character_id': quest.character_id,
            'event_id': quest.event_id,
            'status': quest.status,
            'created_at': quest.created_at.isoformat(),
            'updated_at': quest.updated_at.isoformat()
        }
        for quest in quests
    ]
    return jsonify(quests_data), 200


# 获取角色的所有任务
@main_bp.route('/characters/<int:character_id>/quests', methods=['GET'])
@jwt_required()
def get_character_quests(character_id):
    current_user_id = get_jwt_identity()
    character = Character.query.filter_by(id=character_id, user_id=current_user_id).first()

    if not character:
        return jsonify({'message': 'Character not found.'}), 404

    quests = Quest.query.filter_by(character_id=character.id).all()
    quests_data = [
        {
            'id': quest.id,
            'character_id': quest.character_id,
            'event_id': quest.event_id,
            'status': quest.status,
            'created_at': quest.created_at.isoformat(),
            'updated_at': quest.updated_at.isoformat()
        }
        for quest in quests
    ]
    return jsonify(quests_data), 200


# 更新任务状态
@main_bp.route('/quests/<int:quest_id>', methods=['PUT'])
@jwt_required()
def update_quest(quest_id):
    current_user_id = get_jwt_identity()
    quest = Quest.query.get(quest_id)

    if not quest or quest.character.user_id != current_user_id:
        return jsonify({'message': 'Quest not found.'}), 404

    data = request.get_json()
    status = data.get('status')

    if status not in ['Active', 'Completed', 'Failed']:
        return jsonify({'message': 'Invalid status.'}), 400

    quest.status = status
    db.session.commit()

    return jsonify({'message': 'Quest updated successfully.'}), 200


@main_bp.route('/profile', methods=['GET', 'PUT'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({'message': '用户未找到。'}), 404

    if request.method == 'GET':
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,  # 如果有角色字段
            'created_at': user.created_at.isoformat()
        }
        return jsonify({'user': user_data}), 200

    elif request.method == 'PUT':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if email:
            if User.query.filter(User.email == email, User.id != current_user_id).first():
                return jsonify({'message': '邮箱已被占用。'}), 409
            user.email = email

        if password:
            user.password = password

        db.session.commit()

        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }
        return jsonify({'user': user_data}), 200


# 获取战斗历史记录
@main_bp.route('/battles/history', methods=['GET'])
@jwt_required()
def battle_history():
    current_user_id = get_jwt_identity()
    # 获取用户的所有角色
    characters = Character.query.filter_by(user_id=current_user_id).all()
    character_ids = [char.id for char in characters]
    # 获取这些角色的所有战斗记录
    battles = Battle.query.filter(Battle.character_id.in_(character_ids)).order_by(Battle.created_at.desc()).all()
    battles_data = [
        {
            'id': battle.id,
            'character_id': battle.character_id,
            'event_id': battle.event_id,
            'result': battle.result,
            'experience_gained': battle.experience_gained,
            'items_dropped': battle.items_dropped,
            'created_at': battle.created_at.isoformat()
        }
        for battle in battles
    ]
    return jsonify(battles_data), 200
