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


@inventory_bp.route('/use', methods=['POST'])
def use_item():
    data = request.get_json()
    character_id = data.get('character_id')
    item_id = data.get('item_id')

    if not all([character_id, item_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character_item = CharacterItem.query.filter_by(character_id=character_id, item_id=item_id).first()
    if not character_item:
        return jsonify({'message': '物品不在角色背包中'}), 404

    # 根据物品类型和效果实现使用逻辑
    item = character_item.item
    effect = item.extra_attribute  # 假设使用物品效果在 extra_attribute

    if not effect:
        return jsonify({'message': '该物品无法使用'}), 400

    character = Character.query.get(character_id)

    # 示例：使用药水恢复生命值
    if item.type == '药水':
        heal_amount = effect.get('heal', 0)
        character.health += heal_amount
        # 确保生命值不超过最大值（假设最大值为100 + 额外值）
        character.health = min(character.health, 100 + effect.get('max_health_bonus', 0))
        db.session.commit()
        # 移除药水
        db.session.delete(character_item)
        db.session.commit()
        return jsonify({'message': f'使用{item.name}，恢复了{heal_amount}生命值'}), 200

    # 示例：使用法宝提供增益
    elif item.type == '法宝':
        # 这里需要定义具体的效果，如提升攻击力等
        attack_bonus = effect.get('attack_bonus', 0)
        character.attack += attack_bonus
        db.session.commit()
        # 可能需要添加状态效果或其他逻辑
        return jsonify({'message': f'使用{item.name}，攻击力增加了{attack_bonus}'}), 200

    # 其他物品类型的使用逻辑...

    return jsonify({'message': '物品使用成功'}), 200


@inventory_bp.route('/<int:character_id>', methods=['GET'])
def get_inventory(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    inventory = []
    for ci in character.items:
        item = ci.item
        inventory.append({
            'item_id': item.id,
            'name': item.name,
            'type': item.type,
            'base_attribute': item.base_attribute,
            'extra_attribute': item.extra_attribute,
            'equipped': ci.equipped
        })

    return jsonify({'inventory': inventory}), 200


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
    character_item.equipped = not character_item.equipped
    db.session.commit()

    return jsonify({'message': '物品装备状态已更新', 'equipped': character_item.equipped}), 200
