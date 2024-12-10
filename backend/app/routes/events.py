# backend/app/routes/events.py

from flask import Blueprint, request, jsonify
from ..models import db, Event, Character, Battle, Enemy
import random

events_bp = Blueprint('events', __name__)


@events_bp.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': '事件不存在'}), 404

    event_data = {
        'id': event.id,
        'map_id': event.map_id,
        'description': event.description,
        'event_type': event.event_type,
        'conditions': event.conditions,
        'outcomes': event.outcomes
    }

    return jsonify({'event': event_data}), 200


@events_bp.route('/trigger/<int:event_id>', methods=['POST'])
def trigger_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': '事件不存在'}), 404

    # 根据事件类型处理
    if event.event_type == '战斗':
        battle = Battle.query.filter_by(event_id=event.id).first()
        if not battle:
            return jsonify({'message': '战斗信息未找到'}), 404
        enemy = Enemy.query.get(battle.enemy_id)
        if not enemy:
            return jsonify({'message': '敌人信息未找到'}), 404

        # 返回战斗初始化信息
        battle_data = {
            'battle_id': battle.id,
            'enemy': {
                'id': enemy.id,
                'name': enemy.name,
                'health': enemy.health,
                'attack': enemy.attack,
                'defense': enemy.defense,
                'skills': enemy.skills
            },
            'battle_data': battle.battle_data
        }

        return jsonify({'battle': battle_data}), 200

    elif event.event_type == '剧情':
        # 处理剧情事件
        outcome = event.outcomes
        return jsonify({'outcome': outcome}), 200

    elif event.event_type == '环境':
        # 处理环境事件
        outcome = event.outcomes
        return jsonify({'outcome': outcome}), 200

    else:
        return jsonify({'message': '未知的事件类型'}), 400
