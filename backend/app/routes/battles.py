# backend/app/routes/battles.py

from flask import Blueprint, request, jsonify
from ..models import db, Battle, Enemy, Character, StatusEffect, Skill, CharacterSkill, Item, CharacterItem, Event
from sqlalchemy.exc import IntegrityError
import random

battles_bp = Blueprint('battles', __name__)


@battles_bp.route('/start', methods=['POST'])
def start_battle():
    data = request.get_json()
    character_id = data.get('character_id')
    event_id = data.get('event_id')

    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    event = Event.query.get(event_id)
    if not event:
        return jsonify({'message': '事件不存在'}), 404

    # 根据事件配置选择或生成敌人
    enemy = Enemy.query.get(event.conditions.get('enemy_id'))
    if not enemy:
        return jsonify({'message': '敌人不存在'}), 404

    # 创建新的战斗记录
    battle = Battle(
        event_id=event_id,
        enemy_id=enemy.id,
        character_id=character_id,
        battle_data={
            'player_health': character.health,
            'enemy_health': enemy.health,
            'player_mana': character.mana,
            'turn': 'player',
            'turn_count': 1,
            'action_taken': False,
            'skill_cooldowns': {},
            'status_effects': [],
            'combat_log': ['战斗开始！']
        }
    )

    db.session.add(battle)
    db.session.commit()

    return jsonify({
        'battle_id': battle.id,
        'message': '战斗开始',
        'battle_data': battle.battle_data
    }), 201


@battles_bp.route('/<int:battle_id>', methods=['GET'])
def get_battle(battle_id):
    battle = Battle.query.get(battle_id)
    if not battle:
        return jsonify({'message': '战斗不存在'}), 404

    enemy = battle.enemy
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

    enemy = battle.enemy
    if not enemy:
        return jsonify({'message': '敌人信息未找到'}), 404

    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    # 初始化战斗数据
    if not battle.battle_data:
        battle.battle_data = {
            'player_health': character.health,
            'enemy_health': enemy.health,
            'turn': 'player',  # 'player' or 'enemy'
            'turn_count': 1,
            'action_taken': False  # 新增：标记本回合是否已执行动作
        }

    # 处理状态效果
    active_effects = StatusEffect.query.filter_by(battle_id=battle_id).all()
    for effect in active_effects:
        if effect.effect_type == 'stun' and effect.target == 'player':
            return jsonify({'message': '你被眩晕，无法行动'}), 400
        # 处理其他效果如减速等
        # 这里可以根据需要添加更多状态效果的处理逻辑

    # 获取当前回合
    current_turn = battle.battle_data.get('turn', 'player')

    if current_turn != 'player':
        return jsonify({'message': '当前不是玩家的回合'}), 400

    # 检查是否已经执行过动作
    if battle.battle_data.get('action_taken', False):
        return jsonify({'message': '本回合已执行过动作'}), 400

    # 处理玩家行动
    if action == 'attack':
        damage = max(character.attack - enemy.defense, 0)
        battle.battle_data['enemy_health'] -= damage
        battle.battle_data['last_action'] = {
            'type': 'attack',
            'damage': damage
        }
        battle.battle_data['action_taken'] = True  # 标记动作已执行
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

        # 检查技能冷却
        last_used_turn = battle.battle_data.get(f'skill_{skill_id}_last_used_turn', 0)
        if (battle.battle_data['turn_count'] - last_used_turn) < skill.cooldown:
            remaining_cooldown = skill.cooldown - (battle.battle_data['turn_count'] - last_used_turn)
            return jsonify({'message': f'技能冷却中，剩余{remaining_cooldown}回合'}), 400

        # 扣除法力
        character.mana -= skill.mana_cost

        # 应用技能效果
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
            battle.battle_data['enemy_health'] -= damage
            # 处理额外效果，如眩晕
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
        elif target == 'cone_aoe':
            damage = max(base_damage - enemy.defense, 0)
            battle.battle_data['enemy_health'] -= damage
            # 处理其他效果如出血等
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
        # 处理其他目标类型...

        # 更新技能冷却
        battle.battle_data[f'skill_{skill_id}_last_used_turn'] = battle.battle_data.get('turn_count', 1)

        # 记录最后行动
        battle.battle_data['last_action'] = {
            'type': 'skill',
            'skill_id': skill_id,
            'damage': damage
        }
        battle.battle_data['action_taken'] = True  # 标记动作已执行
    elif action == 'escape':
        # 实现逃跑逻辑
        battle.battle_data['escaped'] = True
        battle.battle_data['result'] = 'escaped'
        db.session.commit()
        return jsonify({'result': 'escaped'}), 200
    else:
        return jsonify({'message': '无效的行动类型'}), 400

    # 检查敌人是否死亡
    if battle.battle_data['enemy_health'] <= 0:
        # 战斗胜利
        battle.battle_data['result'] = 'victory'
        experience_gained = 100  # 示例经验值
        character.experience += experience_gained

        # 处理战斗奖励
        loot = battle.outcomes.get('loot', {})
        if 'experience' in loot:
            character.experience += loot['experience']
        if 'item_ids' in loot:
            for item_id in loot['item_ids']:
                item = Item.query.get(item_id)
                if item:
                    # 检查背包容量
                    current_inventory_count = CharacterItem.query.filter_by(character_id=character_id).count()
                    if current_inventory_count < character.inventory_capacity:
                        new_character_item = CharacterItem(
                            character_id=character_id,
                            item_id=item_id,
                            equipped=False
                        )
                        db.session.add(new_character_item)

        db.session.commit()
        return jsonify({'result': 'victory', 'experience_gained': experience_gained}), 200

    # 敌人的回合
    if not battle.battle_data.get('escaped', False):
        enemy_action = random.choice(['attack', 'skill'])
        if enemy_action == 'attack':
            enemy_damage = max(enemy.attack - character.defense, 0)
            battle.battle_data['player_health'] -= enemy_damage
            battle.battle_data['last_enemy_action'] = {
                'type': 'attack',
                'damage': enemy_damage
            }
        elif enemy_action == 'skill':
            enemy_skills = enemy.skills.get('skills', [])
            if enemy_skills:
                skill_name = random.choice(enemy_skills)
                # 根据技能名称查找技能
                skill = Skill.query.filter_by(name=skill_name, profession='武者').first()  # 假设敌人职业为武者
                if skill and character.mana >= skill.mana_cost:
                    # 扣除法力
                    character.mana -= skill.mana_cost
                    # 应用技能效果
                    effect = skill.effect
                    target = effect.get('target', 'single')
                    damage_type = effect.get('damage_type', 'physical')
                    damage = 0

                    if damage_type == 'physical':
                        base_damage = enemy.attack
                    elif damage_type == 'magic':
                        base_damage = 15  # 示例法术伤害
                    else:
                        base_damage = 0

                    if target == 'single':
                        damage = max(base_damage - character.defense, 0)
                        battle.battle_data['player_health'] -= damage
                        # 处理额外效果，如眩晕
                        if 'stun_chance' in effect and random.random() < effect['stun_chance']:
                            stun_duration = effect.get('stun_duration', 1)
                            status = StatusEffect(
                                battle_id=battle_id,
                                target='character',
                                effect_type='stun',
                                duration=stun_duration,
                                parameters={}
                            )
                            db.session.add(status)
                    elif target == 'cone_aoe':
                        damage = max(base_damage - character.defense, 0)
                        battle.battle_data['player_health'] -= damage
                        # 处理其他效果如出血等
                        if 'bleed' in effect:
                            bleed = effect['bleed']
                            status = StatusEffect(
                                battle_id=battle_id,
                                target='character',
                                effect_type='bleed',
                                duration=bleed['duration'],
                                parameters={'damage_percent_hp': bleed['damage_percent_hp']}
                            )
                            db.session.add(status)
                    # 处理其他目标类型...

                    battle.battle_data['last_enemy_action'] = {
                        'type': 'skill',
                        'skill_name': skill_name,
                        'damage': damage
                    }

        # 检查角色是否死亡
        if battle.battle_data['player_health'] <= 0:
            battle.battle_data['result'] = 'defeat'
            db.session.commit()
            return jsonify({'result': 'defeat'}), 200

    # 更新回合信息
    # 切换回合并重置 action_taken
    if battle.battle_data['turn'] == 'player':
        battle.battle_data['turn'] = 'enemy'
    else:
        battle.battle_data['turn'] = 'player'
        battle.battle_data['turn_count'] = battle.battle_data.get('turn_count', 1) + 1
        battle.battle_data['action_taken'] = False  # 重置动作标记

    db.session.commit()

    return jsonify({
        'result': 'ongoing',
        'player_health': battle.battle_data['player_health'],
        'enemy_health': battle.battle_data['enemy_health'],
        'last_action': battle.battle_data.get('last_action'),
        'last_enemy_action': battle.battle_data.get('last_enemy_action')
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


# 开始战斗
