# backend/app/routes/tasks.py

from flask import Blueprint, request, jsonify
from ..models import db, Task, Character, CharacterTask

tasks_bp = Blueprint('tasks', __name__)


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
        'created_at': task.created_at.isoformat()
    }

    return jsonify({'task': task_data}), 200


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
