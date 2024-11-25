# backend/app/models.py

from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    # password_hash = db.Column(db.Text, nullable=False)
    password = db.Column(db.String())
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('Character', backref='user', lazy=True)
    #
    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    profession = db.Column(db.Enum('Swordmaster', 'Taoist', 'Martial Monk', 'Archer', 'Healer'), nullable=False)
    level = db.Column(db.Integer, default=1)
    strength = db.Column(db.Integer, default=10)
    spirit = db.Column(db.Integer, default=10)
    agility = db.Column(db.Integer, default=10)
    constitution = db.Column(db.Integer, default=10)
    wisdom = db.Column(db.Integer, default=10)
    experience = db.Column(db.Integer, default=0)
    current_map = db.Column(db.String(100), default='长安城')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventories = db.relationship('Inventory', backref='character', lazy=True)
    equipments = db.relationship('Equipment', backref='character', lazy=True)
    battles = db.relationship('Battle', backref='character', lazy=True)
    quests = db.relationship('Quest', backref='character', lazy=True)


class Map(db.Model):
    __tablename__ = 'maps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    json_data = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    events = db.relationship('Event', backref='map', lazy=True)


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    map_id = db.Column(db.Integer, db.ForeignKey('maps.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.Enum('Combat', 'Puzzle', 'Dialogue', 'Quest'), nullable=False)
    conditions = db.Column(db.JSON, nullable=True)
    results = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    battles = db.relationship('Battle', backref='event', lazy=True)
    quests = db.relationship('Quest', backref='event', lazy=True)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum('Weapon', 'Armor', 'Accessory', 'Consumable', 'Special'), nullable=False)
    attributes = db.Column(db.JSON, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inventories = db.relationship('Inventory', backref='item', lazy=True)
    equipments = db.relationship('Equipment', backref='item', lazy=True)


class Inventory(db.Model):
    __tablename__ = 'inventories'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Equipment(db.Model):
    __tablename__ = 'equipments'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    slot = db.Column(db.Enum('Weapon', 'Head', 'Body', 'Legs', 'Accessory'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Battle(db.Model):
    __tablename__ = 'battles'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    result = db.Column(db.Enum('Victory', 'Defeat'), nullable=False)
    experience_gained = db.Column(db.Integer, default=0)
    items_dropped = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Quest(db.Model):
    __tablename__ = 'quests'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    status = db.Column(db.Enum('Active', 'Completed', 'Failed'), nullable=False, default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
