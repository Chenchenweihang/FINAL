# backend/app/routes/battles.py

from flask import Blueprint, request, jsonify
from ..models import db, Battle, Enemy, Character, StatusEffect, Skill, CharacterSkill
from sqlalchemy import and_
import random

battles_bp = Blueprint('battles', __name__)


@battles_bp.route('/<int:battle_id>', methods=['GET'])
def get_battle(battle_id):
    battle = Battle.query.get(battle_id)
    if not battle:
        return jsonify({'message': '战斗不存在'}), 404

    enemy = Enemy.query.get(battle.enemy_id)
    if not enemy:
        return jsonify({'message': '敌人信息未找到'}), 404

    battle_data = {
        'id': battle.id,
        'event_id': battle.event_id,
        'enemy': {
            'id': enemy.id,
            'name': enemy.name,
            'health': enemy.health,
            'attack': enemy.attack,
            'defense': enemy.defense,
            'skills': enemy.skills
        },
        'battle_data': battle.battle_data,
        'status_effects': [
            {
                'id': se.id,
                'target': se.target,
                'effect_type': se.effect_type,
                'duration': se.duration,
                'parameters': se.parameters
            } for se in battle.status_effects
        ]
    }

    return jsonify({'battle': battle_data}), 200


@battles_bp.route('/<int:battle_id>/action', methods=['POST'])
def perform_action(battle_id):
    data = request.get_json()
    action = data.get('action')  # 'attack', 'skill', 'escape'
    character_id = data.get('character_id')
    skill_id = data.get('skill_id')  # 如果使用技能，需要传递 skill_id

    if not all([action, character_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    battle = Battle.query.get(battle_id)
    if not battle:
        return jsonify({'message': '战斗不存在'}), 404

    enemy = Enemy.query.get(battle.enemy_id)
    if not enemy:
        return jsonify({'message': '敌人信息未找到'}), 404

    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    # 简化战斗逻辑：忽略状态效果对行动的影响

    if action == 'attack':
        damage = max(character.attack - enemy.defense, 0)
        enemy.health -= damage
        battle.battle_data['enemy_health'] = enemy.health

        # 检查敌人是否死亡
        if enemy.health <= 0:
            # 战斗胜利
            experience_gained = 100
            character.experience += experience_gained
            # 处理战斗奖励
            loot = battle.battle_data.get('loot', {})
            if 'experience' in loot:
                character.experience += loot['experience']
            if 'item_id' in loot:
                item_id = loot['item_id']
                from ..models import CharacterItem
                # 检查背包容量
                current_inventory_count = CharacterItem.query.filter_by(character_id=character_id).count()
                if current_inventory_count < character.inventory_capacity:
                    character_item = CharacterItem(
                        character_id=character_id,
                        item_id=item_id,
                        equipped=False
                    )
                    db.session.add(character_item)
            db.session.commit()
            return jsonify({'result': 'victory', 'experience_gained': experience_gained}), 200
        else:
            # 敌人反击
            damage_to_player = max(enemy.attack - character.defense, 0)
            character.health -= damage_to_player
            battle.battle_data['player_health'] = character.health

            if character.health <= 0:
                db.session.commit()
                return jsonify({'result': 'defeat'}), 200
            else:
                db.session.commit()
                return jsonify({
                    'result': 'ongoing',
                    'player_health': character.health,
                    'enemy_health': enemy.health
                }), 200

    elif action == 'skill':
        if not skill_id:
            return jsonify({'message': '使用技能时需要提供 skill_id'}), 400

        character_skill = CharacterSkill.query.filter_by(character_id=character_id, skill_id=skill_id).first()
        if not character_skill:
            return jsonify({'message': '角色未学习该技能'}), 404

        skill = Skill.query.get(skill_id)
        if not skill:
            return jsonify({'message': '技能不存在'}), 404

        if character.mana < skill.mana_cost:
            return jsonify({'message': '法力值不足'}), 400

        # 扣除法力
        character.mana -= skill.mana_cost

        # 根据技能效果处理
        effect = skill.effect
        target = effect.get('target', 'single')
        damage_type = effect.get('damage_type', 'physical')
        damage = 0

        if damage_type == 'physical':
            base_damage = character.attack
        elif damage_type == 'magic':
            base_damage = 15  # 假设法术攻击固定伤害
        else:
            base_damage = 0

        if target == 'single':
            damage = max(base_damage - enemy.defense, 0)
            enemy.health -= damage
            # 处理额外效果
            if 'stun_chance' in effect and random.random() < effect['stun_chance']:
                stun_duration = effect.get('stun_duration', 1)
                status = StatusEffect(
                    battle_id=battle_id,
                    target='enemy',
                    effect_type='stun',
                    duration=stun_duration,
                    parameters={}
                )
                db.session.add(status)
        elif target == 'aoe':
            damage = max(base_damage - enemy.defense, 0)
            enemy.health -= damage
            # 处理额外效果，如出血
            if 'bleed' in effect:
                bleed = effect['bleed']
                status = StatusEffect(
                    battle_id=battle_id,
                    target='enemy',
                    effect_type='bleed',
                    duration=bleed['duration'],
                    parameters={'damage_percent_hp': bleed['damage_percent_hp']}
                )
                db.session.add(status)
        elif target == 'cone_aoe':
            # 假设只有一个敌人，类似单体
            damage = max(base_damage - enemy.defense, 0)
            enemy.health -= damage
            if 'stun_duration' in effect:
                status = StatusEffect(
                    battle_id=battle_id,
                    target='enemy',
                    effect_type='stun',
                    duration=effect['stun_duration'],
                    parameters={}
                )
                db.session.add(status)
        elif target == 'wide_aoe':
            damage = max(base_damage - enemy.defense, 0)
            enemy.health -= damage
            if 'attack_speed_reduction' in effect:
                status = StatusEffect(
                    battle_id=battle_id,
                    target='enemy',
                    effect_type='attack_speed_reduction',
                    duration=effect['duration'],
                    parameters={'reduction': effect['attack_speed_reduction']}
                )
                db.session.add(status)
        # 其他目标类型的处理...

        # 检查敌人是否死亡
        if enemy.health <= 0:
            # 战斗胜利
            experience_gained = 100
            character.experience += experience_gained
            # 处理战斗奖励
            loot = battle.battle_data.get('loot', {})
            if 'experience' in loot:
                character.experience += loot['experience']
            if 'item_id' in loot:
                item_id = loot['item_id']
                from ..models import CharacterItem
                # 检查背包容量
                current_inventory_count = CharacterItem.query.filter_by(character_id=character_id).count()
                if current_inventory_count < character.inventory_capacity:
                    character_item = CharacterItem(
                        character_id=character_id,
                        item_id=item_id,
                        equipped=False
                    )
                    db.session.add(character_item)
            db.session.commit()
            return jsonify({'result': 'victory', 'experience_gained': experience_gained, 'damage_dealt': damage}), 200
        else:
            # 敌人反击
            damage_to_player = max(enemy.attack - character.defense, 0)
            character.health -= damage_to_player
            battle.battle_data['player_health'] = character.health

            if character.health <= 0:
                db.session.commit()
                return jsonify({'result': 'defeat'}), 200
            else:
                db.session.commit()
                return jsonify({
                    'result': 'ongoing',
                    'player_health': character.health,
                    'enemy_health': enemy.health,
                    'damage_dealt': damage,
                    'damage_received': damage_to_player
                }), 200


@battles_bp.route('/<int:battle_id>/status', methods=['GET'])
def get_battle_status(battle_id):
    battle = Battle.query.get(battle_id)
    if not battle:
        return jsonify({'message': '战斗不存在'}), 404

    status_effects = [
        {
            'id': se.id,
            'target': se.target,
            'effect_type': se.effect_type,
            'duration': se.duration,
            'parameters': se.parameters
        } for se in battle.status_effects
    ]

    return jsonify({'status_effects': status_effects}), 200
