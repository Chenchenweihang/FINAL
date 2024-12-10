# backend/app/routes/tasks.py

from flask import Blueprint, request, jsonify
from ..models import db, Task, Character, CharacterTask

tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    task_type = data.get('task_type')
    requirements = data.get('requirements')
    rewards = data.get('rewards')

    if not all([name, description, task_type, requirements, rewards]):
        return jsonify({'message': '缺少必要参数'}), 400

    if task_type not in ['主线', '支线']:
        return jsonify({'message': '无效的任务类型'}), 400

    new_task = Task(
        name=name,
        description=description,
        task_type=task_type,
        requirements=requirements,
        rewards=rewards
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'message': '任务创建成功', 'task_id': new_task.id}), 201


@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'message': '任务不存在'}), 404

    task_data = {
        'id': task.id,
        'name': task.name,
        'description': task.description,
        'task_type': task.task_type,
        'requirements': task.requirements,
        'rewards': task.rewards,
        'created_at': task.created_at
    }

    return jsonify({'task': task_data}), 200


@tasks_bp.route('/assign', methods=['POST'])
def assign_task():
    data = request.get_json()
    character_id = data.get('character_id')
    task_id = data.get('task_id')

    if not all([character_id, task_id]):
        return jsonify({'message': '缺少必要参数'}), 400

    character = Character.query.get(character_id)
    task = Task.query.get(task_id)

    if not character:
        return jsonify({'message': '角色不存在'}), 404
    if not task:
        return jsonify({'message': '任务不存在'}), 404

    existing = CharacterTask.query.filter_by(character_id=character_id, task_id=task_id).first()
    if existing:
        return jsonify({'message': '任务已分配给该角色'}), 400

    character_task = CharacterTask(
        character_id=character_id,
        task_id=task_id,
        status='未开始',
        progress={}
    )
    db.session.add(character_task)
    db.session.commit()

    return jsonify({'message': '任务已分配', 'character_task_id': character_task.id}), 201


@tasks_bp.route('/character/<int:character_id>', methods=['GET'])
def get_character_tasks(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({'message': '角色不存在'}), 404

    character_tasks = CharacterTask.query.filter_by(character_id=character_id).all()
    if not character_tasks:
        return jsonify({'message': '未找到角色任务'}), 404

    tasks_data = []
    for ct in character_tasks:
        task = ct.task
        tasks_data.append({
            'character_task_id': ct.id,
            'task_id': task.id,
            'name': task.name,
            'description': task.description,
            'task_type': task.task_type,
            'status': ct.status,
            'progress': ct.progress
        })

    return jsonify({'character_tasks': tasks_data}), 200


@tasks_bp.route('/update/<int:character_task_id>', methods=['PUT'])
def update_character_task(character_task_id):
    data = request.get_json()
    status = data.get('status')
    progress = data.get('progress')

    if not status:
        return jsonify({'message': '缺少状态参数'}), 400

    if status not in ['未开始', '进行中', '已完成']:
        return jsonify({'message': '无效的状态'}), 400

    character_task = CharacterTask.query.get(character_task_id)
    if not character_task:
        return jsonify({'message': '角色任务不存在'}), 404

    character_task.status = status
    if progress:
        character_task.progress = progress

    db.session.commit()

    return jsonify({'message': '任务状态已更新'}), 200
