# backend/app/routes/skills.py

from flask import Blueprint, request, jsonify
from ..models import db, Skill, Character, CharacterSkill

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/<profession>', methods=['GET'])
def get_skills(profession):
    if profession not in ['剑侠', '武者', '刺客', '道士']:
        return jsonify({'message': '无效的职业'}), 400

    skills = Skill.query.filter_by(profession=profession).all()

    if not skills:
        return jsonify({'message': '未找到技能'}), 404

    skills_data = []
    for skill in skills:
        skills_data.append({
            'id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'level_required': skill.level_required,
            'cooldown': skill.cooldown,
            'mana_cost': skill.mana_cost,
            'effect': skill.effect
        })

    return jsonify({'skills': skills_data}), 200


@skills_bp.route('/learn', methods=['POST'])
def learn_skill():
    data = request.get_json()
    character_id = data.get('character_id')
    skill_id = data.get('skill_id')

    if not all([character_id, skill_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character = Character.query.get(character_id)
    skill = Skill.query.get(skill_id)

    if not character:
        return jsonify({'message': '角色不存在'}), 404
    if not skill:
        return jsonify({'message': '技能不存在'}), 404
    if skill.profession != character.profession:
        return jsonify({'message': '技能职业不匹配'}), 400
    if character.level < skill.level_required:
        return jsonify({'message': '角色等级不足以学习该技能'}), 400

    existing = CharacterSkill.query.filter_by(character_id=character_id, skill_id=skill_id).first()
    if existing:
        return jsonify({'message': '角色已学习该技能'}), 400

    character_skill = CharacterSkill(
        character_id=character_id,
        skill_id=skill_id
    )
    db.session.add(character_skill)
    db.session.commit()

    return jsonify({'message': '技能学习成功', 'character_skill_id': character_skill.id}), 201


@skills_bp.route('/character/<int:character_id>', methods=['GET'])
def get_character_skills(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    character_skills = CharacterSkill.query.filter_by(character_id=character_id).all()
    skills_data = []
    for cs in character_skills:
        skill = cs.skill
        skills_data.append({
            'character_skill_id': cs.id,
            'skill_id': skill.id,
            'name': skill.name,
            'description': skill.description,
            'level_required': skill.level_required,
            'cooldown': skill.cooldown,
            'mana_cost': skill.mana_cost,
            'effect': skill.effect
        })

    return jsonify({'character_skills': skills_data}), 200
