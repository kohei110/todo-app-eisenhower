from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from flask import g

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(os.path.join(app.root_path, 'tasks.db'))
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/add', methods=['POST'])
def add_task():
    # Add code to add a new task
    pass

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    # Add code to update a task
    pass

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    # Add code to delete a task
    pass

if __name__ == '__main__':
    init_db()
    app.run(debug=True)