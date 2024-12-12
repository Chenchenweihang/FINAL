# backend/app/routes/items.py

from flask import Blueprint, request, jsonify
from ..models import db, Item, Set
from sqlalchemy.exc import IntegrityError

items_bp = Blueprint('items', __name__)


@items_bp.route('/', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    items_data = []
    for item in items:
        if item.extra_attribute is None:
            item.extra_attribute = '非法宝装备无额外技能'
        print(item.base_attribute)
        print(item.extra_attribute)
        items_data.append({
            'id': item.id,
            'name': item.name,
            'type': item.type,
            'base_attribute': item.base_attribute,
            'extra_attribute': item.extra_attribute,
            'set_id': item.set_id
        })
    return jsonify({'items': items_data}), 200


@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': '物品不存在'}), 404

    item_data = {
        'id': item.id,
        'name': item.name,
        'type': item.type,
        'base_attribute': item.base_attribute,
        'extra_attribute': item.extra_attribute,
        'set_id': item.set_id
    }

    return jsonify({'item': item_data}), 200


@items_bp.route('/create', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    type_ = data.get('type')
    base_attribute = data.get('base_attribute')
    extra_attribute = data.get('extra_attribute')
    set_id = data.get('set_id')

    if not all([name, type_, base_attribute]):
        return jsonify({'message': '缺少必要参数'}), 400

    if type_ not in ['武器', '防具', '饰品', '法宝']:
        return jsonify({'message': '无效的物品类型'}), 400

    if set_id:
        set_ = Set.query.get(set_id)
        if not set_:
            return jsonify({'message': '套装不存在'}), 404

    new_item = Item(
        name=name,
        type=type_,
        base_attribute=base_attribute,
        extra_attribute=extra_attribute,
        set_id=set_id
    )

    try:
        db.session.add(new_item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '物品创建失败'}), 500

    return jsonify({'message': '物品创建成功', 'item_id': new_item.id}), 201


@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': '物品不存在'}), 404

    data = request.get_json()
    name = data.get('name')
    type_ = data.get('type')
    base_attribute = data.get('base_attribute')
    extra_attribute = data.get('extra_attribute')
    set_id = data.get('set_id')

    if type_ and type_ not in ['武器', '防具', '饰品', '法宝']:
        return jsonify({'message': '无效的物品类型'}), 400

    if set_id:
        set_ = Set.query.get(set_id)
        if not set_:
            return jsonify({'message': '套装不存在'}), 404

    if name:
        item.name = name
    if type_:
        item.type = type_
    if base_attribute:
        item.base_attribute = base_attribute
    if 'extra_attribute' in data:
        item.extra_attribute = extra_attribute
    if 'set_id' in data:
        item.set_id = set_id

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '物品更新失败'}), 500

    return jsonify({'message': '物品信息已更新'}), 200


@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'message': '物品不存在'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': '物品删除失败'}), 500

    return jsonify({'message': '物品已删除'}), 200
