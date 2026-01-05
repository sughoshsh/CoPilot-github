from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todotest.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    done = db.Column(db.Boolean, default=False)

    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('app.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
    return jsonify({'message': 'Todo added successfully!'})

@app.route('/update/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.title = request.form.get('title', todo.title)
    todo.description = request.form.get('description', todo.description)
    todo.done = request.form.get('done', str(todo.done)).lower() == 'true'
    db.session.commit()
    return jsonify({'message': 'Todo updated successfully!'})

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)