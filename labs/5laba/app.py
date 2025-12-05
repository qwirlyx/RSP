from flask import Flask, request, jsonify
app = Flask(__name__)

tasks = []
task_id_counter = 1


@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return jsonify(task)
    return jsonify({'error': 'Задача не найдена'}), 404


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()

    new_task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'completed': False
    }

    tasks.append(new_task)
    task_id_counter += 1

    return jsonify(new_task), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data.get('title', task['title'])
            task['completed'] = data.get('completed', task['completed'])
            return jsonify(task)

    return jsonify({'error': 'Задача не найдена'}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            return jsonify({'message': 'Задача удалена'})

    return jsonify({'error': 'Задача не найдена'}), 404


if __name__ == '__main__':
    app.run(debug=True)
