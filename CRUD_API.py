from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize the app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Book Model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __init__(self, book_name, author, publisher):
        self.book_name = book_name
        self.author = author
        self.publisher = publisher

# Book Schema
class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'book_name', 'author', 'publisher')

# Initialize schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

# Routes
# Create a new book
@app.route('/book', methods=['POST'])
def add_book():
    book_name = request.json['book_name']
    author = request.json['author']
    publisher = request.json['publisher']
    
    new_book = Book(book_name, author, publisher)
    db.session.add(new_book)
    db.session.commit()
    
    return book_schema.jsonify(new_book)

# Get all books
@app.route('/book', methods=['GET'])
def get_books():
    all_books = Book.query.all()
    return books_schema.jsonify(all_books)

# Get a single book
@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return book_schema.jsonify(book)

# Update a book
@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    book_name = request.json.get('book_name', book.book_name)
    author = request.json.get('author', book.author)
    publisher = request.json.get('publisher', book.publisher)

    book.book_name = book_name
    book.author = author
    book.publisher = publisher

    db.session.commit()
    return book_schema.jsonify(book)

# Delete a book
@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

# Run the app
if __name__ == '__main__':
    # Create the database
    if not os.path.exists('books.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)
