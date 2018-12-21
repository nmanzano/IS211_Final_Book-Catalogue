from flask import (Flask, session, render_template,
                   request, redirect, g, url_for)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (Table, Column, Float,
                        Integer, String, MetaData, ForeignKey)
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books_library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Username(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(6), unique=True, nullable=False)
    password = Column(String(20))
    books = db.relationship('Books', backref='owner')

    def __repr__(self):
        return '<User %r>' % self.username


class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    page_count = db.Column(db.Integer)
    average_rating = db.Column(db.String(30), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('username.id'))


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)
        username = (Username.query.filter(
                                Username.username == request.form['username']
                            ).first())
        if username:
            if request.form['password'] == username.password:
                session['password'] = request.form['password']
                session['user'] = request.form['username']
                return redirect(url_for('dashboard'))
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if g.user:
        if request.method == 'GET':
            username = Username.query.filter(
                Username.username == g.user
            ).first()
            books = Books.query.filter(username.id == Books.owner_id).all()
            print(books, 'this is the books')
        return render_template('dashboard.html', books=books)
    return redirect(url_for('login'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if g.user:
        if request.method == 'GET':
            return render_template('add_book.html')
        if request.method == 'POST':
            username = Username.query.filter(
                Username.username == g.user
            ).first()

            new_book = Books(title=request.form['title'],
                             author=request.form['author'],
                             page_count=request.form['page_count'],
                             average_rating=request.form['rating'],
                             owner_id=username.id)
            db.session.add(new_book)
            db.session.commit()
            db.session.close()
            return render_template('add_book.html')
    return redirect(url_for('login'))


@app.route('/delete_book', methods=['POST'])
def delete_book():
    if g.user:
        if request.method == 'POST':
            print(request.form['book_id'], 'this is line 89')
            book_id = Books.query.filter(
                Books.id == request.form['book_id']
            ).first()
            print(book_id, 'this is line 95')
            db.session.delete(book_id)
            db.session.commit()
            db.session.close()
    return redirect(url_for('dashboard'))


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        credentials = (Username(username=request.form['username'],
                                password=request.form['password']))
        db.session.add(credentials)
        db.session.commit()
        db.session.close()
        return redirect(url_for('login'))
    return render_template('create_user.html')


if __name__ == '__main__':
    app.run(debug=True)
