import unittest
import json
from dbModels import Book, Review
from DbConntection import app, db
import main

class BookApiTestCase(unittest.TestCase):

    def setUp(self):
        # Setup before each test
         app.config['TESTING'] = True
         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # in-memory test DB
         app.config['CACHE_TYPE'] = 'null'  # Disable caching for tests
         self.client = app.test_client()
        
         with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_book(self):
        print("Starting test_add_book")
        response = self.client.post('/books', json={
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'description': 'A book about building habits'
        })
        print('heellooo',response.status_code, response.get_data(as_text=True))  # Add this line
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully', response.get_data(as_text=True))

    def test_get_books(self):
        # Insert one book first
        with app.app_context():
            book = Book(title='Deep Work', author='Cal Newport', description='Productivity')
            db.session.add(book)
            db.session.commit()

        response = self.client.get('/books')
        print(response.status_code, response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Deep Work', response.get_data(as_text=True))

    
if __name__ == '__main__':
    unittest.main()
