import os

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(BASE_DIR, 'books.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# Модель книги
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)

# Главная страница (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Страница со списком книг (books.html)
@app.route('/books')
def books_page():
    books = Book.query.all()
    return render_template('books.html', books=books)

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

if __name__ == '__main__':
    # Создание таблиц в базе данных перед запуском сервера
    with app.app_context():
        print("Создаем таблицы в базе данных...")
        db.create_all()
        print("Таблицы созданы!")

    # Запуск приложения
    app.run(debug=True)
