# backend/app/routes/maps.py

from flask import Blueprint, request, jsonify
from ..models import db, Map

maps_bp = Blueprint('maps', __name__)


@maps_bp.route('/', methods=['GET'])
def get_maps():
    parent_map = request.args.get('parent_map')  # 可选参数，过滤某个上属地图

    if parent_map:
        maps = Map.query.filter_by(parent_map=parent_map).all()
    else:
        maps = Map.query.all()

    if not maps:
        return jsonify({'message': '未找到地图'}), 404

    maps_data = []
    for m in maps:
        maps_data.append({
            'id': m.id,
            'name': m.name,
            'description': m.description,
            'level_required': m.level_required,
            'parent_map': m.parent_map
        })

    return jsonify({'maps': maps_data}), 200


@maps_bp.route('/<int:map_id>', methods=['GET'])
def get_map(map_id):
    m = Map.query.get(map_id)
    if not m:
        return jsonify({'message': '地图不存在'}), 404

    map_data = {
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'level_required': m.level_required,
        'parent_map': m.parent_map
    }

    return jsonify({'map': map_data}), 200
