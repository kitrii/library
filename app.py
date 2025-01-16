import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)


# Модель пользователя
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


# Загрузка пользователя из базы данных
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Регистрация пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

# Авторизация пользователя
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Неверные учетные данные', 401
    return render_template('login.html')


# Выход из системы
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Пример защищенного маршрута
@app.route('/protected')
@login_required
def protected():
    return f'Добро пожаловать, {current_user.username}!'


# Главная страница (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Страница со списком книг (books.html)
@app.route('/books')
def books_page():
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/add_book')
def add_book_page():
    return render_template('add_book.html')


# Роут для добавления книги через API
@app.route('/api/books', methods=['POST'])
def add_book():
    try:
        data = request.json
        print(f"Полученные данные: {data}")  # Лог данных
        new_book = Book(
            title=data['title'],
            author=data['author'],
            description=data['description'],
            year=data['year']
        )
        db.session.add(new_book)
        db.session.commit()
        print("Книга успешно добавлена!")
        return jsonify({'message': 'Book added successfully!'}), 201
    except Exception as e:
        print(f"Ошибка при добавлении книги: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Книга не найдена'}), 404

        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Книга успешно удалена'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/cookie_policy')
def cookie_policy():
    return render_template('cookie_policy.html')

if __name__ == '__main__':
    # Создание таблиц в базе данных перед запуском сервера
    with app.app_context():
        print("Создаем таблицы в базе данных...")
        db.create_all()
        print("Таблицы созданы!")

    # Запуск приложения
    app.run(debug=True)


