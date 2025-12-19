from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import redis
import json

app = Flask(__name__)

# Подключение к БД (берёт из переменной окружения, fallback для Compose)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql://user:password@db:5432/todo_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Подключение к Redis
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_client = redis.Redis(host=redis_host, port=6379, db=0)

# Модель задачи
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'description': self.description}

# Создание таблиц при старте
with app.app_context():
    db.create_all()

# Главная страница (чтобы в браузере было красиво)
@app.route('/')
def index():
    return '''
    <h1>ToDo List API — Лабораторная работа №7 по Docker</h1>
    <p><strong>Доступные endpoints:</strong></p>
    <ul>
        <li><code>GET /tasks</code> — список всех задач</li>
        <li><code>POST /tasks</code> (JSON: {"description": "текст"}) — добавить задачу</li>
        <li><code>DELETE /tasks/&lt;id&gt;</code> — удалить задачу по id</li>
    </ul>
    <p>Пример добавления задачи через curl:</p>
    <pre>curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"description":"Сделать лабу"}'</pre>
    '''

@app.route('/tasks', methods=['GET'])
def get_tasks():
    # Пробуем взять из кэша Redis
    cached = redis_client.get('tasks_cache')
    if cached:
        return jsonify(json.loads(cached))

    # Если нет — берём из БД
    tasks = Task.query.all()
    tasks_list = [task.to_dict() for task in tasks]
    
    # Сохраняем в кэш на 60 секунд
    redis_client.set('tasks_cache', json.dumps(tasks_list), ex=60)
    
    return jsonify(tasks_list)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or 'description' not in data:
        return jsonify({'error': 'description required'}), 400
    
    task = Task(description=data['description'])
    db.session.add(task)
    db.session.commit()
    
    # Инвалидируем кэш
    redis_client.delete('tasks_cache')
    
    return jsonify(task.to_dict()), 201

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    db.session.delete(task)
    db.session.commit()
    
    # Инвалидируем кэш
    redis_client.delete('tasks_cache')
    
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)