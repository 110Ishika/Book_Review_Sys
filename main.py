from flask import Flask, request, jsonify
from DbConntection import app, db,cache
from dbModels import Book, Review


# --- Routes ---

# Add a book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json #get the requesrt data
    title = data.get('title')
    existBook=Book.query.filter_by(title=title).first()
    if  existBook:
        return jsonify({"error": "Book already exists"}), 400

    book =Book(
      title=title,
      author=data.get('author'),
      description=data.get('description')
     )
    db.session.add(book)
    db.session.commit()

     # Clear cached book list : we acn comment this line if we want to keep the cache
    # This is useful if we want to keep the cache for performance reasons
    cache.delete_memoized('list_books')

    return jsonify({"message": "Book added successfully"}), 201

# List all books
@app.route('/books', methods=['GET'])
@cache.cached(timeout=60)
def list_books():
    books = Book.query.all()
    books_list = []
    print("Listing all books")
    if not books:
        return jsonify({"message": "No books available"}), 200
    for book in books:
        print(f"Title: {book.title}, Author: {book.author}")
        books_list.append({
            "id" : book.id,
            "title" : book.title,
            "author":book.author,
            "description": book.description,
        })
    return jsonify(books_list), 200

# Get details of a specific book
@app.route('/books/<string:title>', methods=['GET'])
def get_book(title):
    books = Book.query.all()
    books_list = []
    if not books:
        return jsonify({"error": "No books available"}), 404

    book = Book.query.filter_by(title=title).first()
    books_list.append({
            "id" : book.id,
             "title" : book.title,
             "author":book.author,
             "description": book.description,
            })

    if  books_list:
        return jsonify(books_list), 200

    return jsonify({"message": "book Not found"}), 200

# Add a review to a book
@app.route('/books/<int:id>/reviews', methods=['POST'])
def add_review(id):
    book = Book.query.filter_by(id=id).first()
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books=[]
    review = request.json
    review = Review(
        reviewer=review.get("reviewer"),
        rating=review.get("rating"),
        comment=review.get("comment"),
        book_id=book.id
    )
    
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review added successfully"}), 201

#Test
@app.route('/books/<int:id>/reviews', methods=['GET'])
def get_review(id):
    Reviews = Review.query.all()
    book=Book.query.filter_by(id=id).first()
    currentId=book.id
    if not book:
        return jsonify({"error": "Book not found"}), 404

    addReview=[]
    for review in Reviews:
            if(review.book_id==currentId):
              addReview.append({
             "id" : review.id,
             "reviewer" : review.reviewer,
             "rating": review.rating,
             "comment": review.comment,
             "book_id": review.id
             }) 

    if addReview:
        return jsonify(addReview), 200

    return jsonify({"message": "book Not found"}), 200

     
 

# Run app
if __name__ == '__main__':
    app.run(debug=True)
