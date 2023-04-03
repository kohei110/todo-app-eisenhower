# https://tech-diary.net/flask-introduction/

from datetime import datetime, date
from flask import Flask, render_template, request, redirect , url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(30), nullable=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        posts = Post.query.order_by(Post.due).all()
        categories = set([post.category for post in posts])
        posts_by_category = {category: [post for post in posts if post.category == category] for category in categories}
        return render_template('index.html', posts_by_category=posts_by_category, categories=categories, today=date.today())

    else:
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        category = request.form.get('category')        
        due = datetime.strptime(due,'%Y-%m-%d')
        
        new_post = Post(title = title, detail = detail, due = due, category = category)

        db.session.add(new_post)
        db.session.commit()

        return redirect('/')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        
        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')    

@app.route('/landing', methods=['GET', 'POST'])
def login():
        return render_template('landing.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/logout')
def create():
    return render_template('logout.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id)
    return render_template('detail.html', post=post)

@app.route('/delete/<int:id>')
def delete(id):
        task = Post.query.get(id)

        db.session.delete(task)
        db.session.commit()    

        return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')
        post.category = request.form.get('category')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)