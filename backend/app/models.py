# backend/app/models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # 生产环境请使用哈希加密
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    characters = db.relationship('Character', backref='user', lazy=True)

class Character(db.Model):
    __tablename__ = 'Characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    profession = db.Column(db.Enum('剑侠', '武者', '医士', '刺客', '道士'), nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    health = db.Column(db.Integer, default=100)
    attack = db.Column(db.Integer, default=10)
    defense = db.Column(db.Integer, default=5)
    mana = db.Column(db.Integer, default=50)
    inventory_capacity = db.Column(db.Integer, default=20)  # 新增：背包容量
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('CharacterItem', backref='character', lazy=True)
    skills = db.relationship('CharacterSkill', backref='character', lazy=True)
    tasks = db.relationship('CharacterTask', backref='character', lazy=True)

class Skill(db.Model):
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.Enum('剑侠', '武者', '医士', '刺客', '道士'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level_required = db.Column(db.Integer, nullable=False)
    cooldown = db.Column(db.Integer, nullable=False)
    mana_cost = db.Column(db.Integer, nullable=False)
    effect = db.Column(db.JSON, nullable=False)

class CharacterSkill(db.Model):
    __tablename__ = 'CharacterSkills'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skills.id'), nullable=False)
    level = db.Column(db.Integer, default=1)  # 技能等级
    __table_args__ = (db.UniqueConstraint('character_id', 'skill_id', name='_character_skill_uc'),)
    skill = db.relationship('Skill', backref='character_skills')

class Set(db.Model):
    __tablename__ = 'Sets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    bonus = db.Column(db.JSON, nullable=False)
    items = db.relationship('Items', backref='set', lazy=True)

class Item(db.Model):
    __tablename__ = 'Items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum('武器', '防具', '饰品', '法宝', '药水'), nullable=False)
    base_attribute = db.Column(db.JSON, nullable=False)
    extra_attribute = db.Column(db.JSON, nullable=True)
    set_id = db.Column(db.Integer, db.ForeignKey('Sets.id'), nullable=True)
    character_items = db.relationship('CharacterItem', backref='item', lazy=True)

class CharacterItem(db.Model):
    __tablename__ = 'CharacterItems'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Items.id'), nullable=False)
    equipped = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint('character_id', 'item_id', name='_character_item_uc'),)

class Map(db.Model):
    __tablename__ = 'Maps'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    level_required = db.Column(db.Integer, nullable=False)
    parent_map = db.Column(db.String(80), nullable=False)
    events = db.relationship('Event', backref='map', lazy=True)

class Event(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    map_id = db.Column(db.Integer, db.ForeignKey('Maps.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.Enum('战斗', '剧情', '环境'), nullable=False)
    conditions = db.Column(db.JSON, nullable=False)
    outcomes = db.Column(db.JSON, nullable=False)
    battles = db.relationship('Battle', backref='event', lazy=True)

class Enemy(db.Model):
    __tablename__ = 'Enemies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    health = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    skills = db.Column(db.JSON, nullable=False)
    battles = db.relationship('Battle', backref='enemy', lazy=True)

class Battle(db.Model):
    __tablename__ = 'Battles'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('Events.id'), nullable=False)
    enemy_id = db.Column(db.Integer, db.ForeignKey('Enemies.id'), nullable=False)
    battle_data = db.Column(db.JSON, nullable=False)
    status_effects = db.relationship('StatusEffect', backref='battle', lazy=True)

class StatusEffect(db.Model):
    __tablename__ = 'StatusEffects'
    id = db.Column(db.Integer, primary_key=True)
    battle_id = db.Column(db.Integer, db.ForeignKey('Battles.id'), nullable=False)
    target = db.Column(db.String(80), nullable=False)  # 'character' 或 'enemy'
    effect_type = db.Column(db.String(80), nullable=False)  # 如 'stun', 'bleed'
    duration = db.Column(db.Integer, nullable=False)  # 持续回合数
    parameters = db.Column(db.JSON, nullable=True)  # 额外参数，如伤害百分比等

class Task(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    task_type = db.Column(db.Enum('主线', '支线'), nullable=False)
    requirements = db.Column(db.JSON, nullable=False)  # 任务要求
    rewards = db.Column(db.JSON, nullable=False)  # 任务奖励
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    character_tasks = db.relationship('CharacterTask', backref='task', lazy=True)

class CharacterTask(db.Model):
    __tablename__ = 'CharacterTasks'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'), nullable=False)
    status = db.Column(db.Enum('未开始', '进行中', '已完成'), default='未开始', nullable=False)
    progress = db.Column(db.JSON, nullable=True)  # 任务进度详情
    __table_args__ = (db.UniqueConstraint('character_id', 'task_id', name='_character_task_uc'),)
