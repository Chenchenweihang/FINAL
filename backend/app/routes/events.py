# backend/app/routes/events.py

from flask import Blueprint, request, jsonify
from ..models import db, Event, Battle, Item, CharacterItem

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

    # 根据事件类型触发不同的逻辑
    if event.event_type == '战斗':
        # 创建战斗记录
        battle = Battle(
            event_id=event.id,
            enemy_id=event.outcomes.get('enemy_id'),
            battle_data={}
        )
        db.session.add(battle)
        db.session.commit()

        battle_data = {
            'battle_id': battle.id,
            'enemy': {
                'id': battle.enemy.id,
                'name': battle.enemy.name,
                'health': battle.enemy.health,
                'attack': battle.enemy.attack,
                'defense': battle.enemy.defense,
                'skills': battle.enemy.skills
            },
            'battle_data': battle.battle_data
        }

        return jsonify({'battle': battle_data}), 200

    elif event.event_type in ['剧情', '环境']:
        outcome = event.outcomes
        reward = outcome.get('reward')
        if reward:
            item_id = reward.get('item_id')
            if item_id:
                # 假设角色ID为1，实际应从请求或上下文中获取
                character_id = request.json.get('character_id')
                if not character_id:
                    return jsonify({'message': '缺少 character_id 参数来接收奖励'}), 400

                character_item = CharacterItem.query.filter_by(character_id=character_id, item_id=item_id).first()
                if character_item:
                    return jsonify({'message': '角色已拥有该物品'}), 400
                else:
                    new_character_item = CharacterItem(
                        character_id=character_id,
                        item_id=item_id,
                        equipped=False
                    )
                    db.session.add(new_character_item)
                    db.session.commit()
                    return jsonify({'outcome': {'reward': {'item_id': item_id}}}), 200
        return jsonify({'outcome': outcome}), 200
    else:
        return jsonify({'message': '未知的事件类型'}), 400
