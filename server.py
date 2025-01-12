from flask import Flask, jsonify, request

app = Flask(__name__)

# Пример данных (хранилище книг)
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949, "description": "Dystopian novel."},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960, "description": "Classic of modern American literature."}
]

# Получить список всех книг
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify(books)

# Добавить новую книгу
@app.route('/api/books', methods=['POST'])
def add_book():
    new_book = request.json
    new_book['id'] = max(book['id'] for book in books) + 1 if books else 1  # Генерация ID
    books.append(new_book)
    return jsonify({"message": "Book added successfully", "book": new_book}), 201

# Удалить книгу по ID
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['id'] != book_id]
    return jsonify({"message": f"Book with ID {book_id} deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
