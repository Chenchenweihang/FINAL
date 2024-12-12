# backend/app/routes/inventory.py

from flask import Blueprint, request, jsonify
from ..models import db, Character, Item, CharacterItem

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/add', methods=['POST'])
def add_item_to_inventory():
    data = request.get_json()
    character_id = data.get('character_id')
    item_id = data.get('item_id')

    if not all([character_id, item_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character = Character.query.get(character_id)
    item = Item.query.get(item_id)

    if not character:
        return jsonify({'message': '角色不存在'}), 404
    if not item:
        return jsonify({'message': '物品不存在'}), 404

    # 检查背包容量
    current_inventory_count = CharacterItem.query.filter_by(character_id=character_id).count()
    if current_inventory_count >= character.inventory_capacity:
        return jsonify({'message': '背包已满'}), 400

    # 检查角色是否已经拥有该物品
    existing = CharacterItem.query.filter_by(character_id=character_id, item_id=item_id).first()
    if existing:
        return jsonify({'message': '角色已拥有该物品'}), 400

    character_item = CharacterItem(
        character_id=character_id,
        item_id=item_id,
        equipped=False
    )
    db.session.add(character_item)
    db.session.commit()

    return jsonify({'message': '物品已添加到背包'}), 201

@inventory_bp.route('/remove', methods=['POST'])
def remove_item_from_inventory():
    data = request.get_json()
    character_id = data.get('character_id')
    item_id = data.get('item_id')

    if not all([character_id, item_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character_item = CharacterItem.query.filter_by(character_id=character_id, item_id=item_id).first()
    if not character_item:
        return jsonify({'message': '物品不在角色背包中'}), 404

    db.session.delete(character_item)
    db.session.commit()

    return jsonify({'message': '物品已从背包中移除'}), 200

@inventory_bp.route('/equipped/<int:character_id>', methods=['GET'])
def get_equipped_items(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    equipped_items = CharacterItem.query.filter_by(character_id=character_id, equipped=True).all()
    items_data = []
    for ci in equipped_items:
        item = ci.item
        items_data.append({
            'item_id': item.id,
            'name': item.name,
            'type': item.type,
            'base_attribute': item.base_attribute,
            'extra_attribute': item.extra_attribute
        })

    return jsonify({'equipped_items': items_data}), 200

@inventory_bp.route('/unequipped/<int:character_id>', methods=['GET'])
def get_unequipped_items(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    unequipped_items = CharacterItem.query.filter_by(character_id=character_id, equipped=False).all()
    items_data = []
    for ci in unequipped_items:
        item = ci.item
        items_data.append({
            'item_id': item.id,
            'name': item.name,
            'type': item.type,
            'base_attribute': item.base_attribute,
            'extra_attribute': item.extra_attribute
        })

    return jsonify({'unequipped_items': items_data}), 200

@inventory_bp.route('/equip', methods=['POST'])
def equip_item():
    data = request.get_json()
    character_id = data.get('character_id')
    item_id = data.get('item_id')

    if not all([character_id, item_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character = Character.query.get(character_id)
    item = Item.query.get(item_id)

    if not character:
        return jsonify({'message': '角色不存在'}), 404
    if not item:
        return jsonify({'message': '物品不存在'}), 404

    character_item = CharacterItem.query.filter_by(character_id=character_id, item_id=item_id).first()
    if not character_item:
        return jsonify({'message': '物品不在角色背包中'}), 404

    # 切换装备状态
    if not character_item.equipped:
        # 检查是否有同类型已装备的物品
        equipped_same_type = CharacterItem.query.join(Item).filter(
            CharacterItem.character_id == character_id,
            Item.type == item.type,
            CharacterItem.equipped == True
        ).first()
        if equipped_same_type:
            # 卸下已装备的同类型物品
            equipped_same_type.equipped = False
        # 装备新物品
        character_item.equipped = True
    else:
        # 卸下物品
        character_item.equipped = False

    db.session.commit()

    return jsonify({'message': '物品装备状态已更新', 'equipped': character_item.equipped}), 200

@inventory_bp.route('/capacity/<int:character_id>', methods=['GET'])
def get_inventory_capacity(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    current_inventory_count = CharacterItem.query.filter_by(character_id=character_id).count()
    remaining_capacity = character.inventory_capacity - current_inventory_count

    return jsonify({
        'inventory_capacity': character.inventory_capacity,
        'current_inventory_count': current_inventory_count,
        'remaining_capacity': remaining_capacity
    }), 200
