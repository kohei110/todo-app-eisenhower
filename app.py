from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        todo_title = request.form['title']
        new_todo = Todo(title=todo_title)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"

    else:
        todos = Todo.query.order_by(Todo.id).all()
        return render_template('index.html', todos=todos)

@app.route('/delete/<int:id>')
def delete(id):
    todo_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

if __name__ == "__main__":
    with app.app_context():  # Add this line to set up an application context
        db.create_all()  # Create the table within the application context
    app.run(debug=True)