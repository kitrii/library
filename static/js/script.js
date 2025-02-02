// static/js/script.js
async function showBooks() {
    const res = await fetch('/books');
    const books = await res.json();
    const list = books.map(book => `
        <div>
            <h3>${book.title}</h3>
            <p>Автор: ${book.author}</p>
            <p>${book.description}</p>
            <p>Год публикации: ${book.year}</p>
        </div>
    `).join('');
    document.getElementById('book-list').innerHTML = list;
    document.getElementById('add-book-form').style.display = 'none';
}

function showAddBookForm() {
    document.getElementById('add-book-form').style.display = 'block';
    document.getElementById('book-list').innerHTML = '';
}

async function addBook() {
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const description = document.getElementById('description').value;
    const year = document.getElementById('year').value;

    await fetch('api//books', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author, description, year })
    });

    alert('Книга добавлена!');
    showBooks();
}

async function deleteBook(bookId) {
    const confirmDelete = confirm('Вы уверены, что хотите удалить эту книгу?');
    if (!confirmDelete) return;

    try {
        const response = await fetch(`/api/books/${bookId}`, {
            method: 'DELETE',
        });

        if (response.ok) {
            alert('Книга успешно удалена!');
            document.querySelector(`.book-card[data-id="${bookId}"]`).remove();
        } else {
            const error = await response.json();
            alert(`Ошибка при удалении книги: ${error.message}`);
        }
    } catch (err) {
        console.error('Ошибка при удалении книги:', err);
        alert('Произошла ошибка. Попробуйте снова.');
    }
}