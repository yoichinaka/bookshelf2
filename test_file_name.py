import unittest
import json
from flaskr import create_app
from models import setup_db, Book

class ResourceTestCase(unittest.TestCase):
    """This class represents the resource test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf"
        self.database_path = 'postgres://yoichi2@localhost:5432/bookshelf'
        setup_db(self.app, self.database_path)

        self.new_book ={
            'title': 'tree',
            'author': 'basho',
            'rating': 5
        }
    
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_given_behavior(self):
        """Test _____________ """
        res = self.client().get('/books')

        self.assertEqual(res.status_code, 200)
    
    def test_get_paginated_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data["books"]))

    def test_404_send_beyond_requesting_books(self):
        res = self.client().get('/books?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "resource not found")
    
    def test_update_book(self):
        res = self.client().patch('/books/1', json={'rating': 2})
        data = json.loads(res.data)
        book = Book.query.filter(Book.id == 1).one_or_none()

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(book.format()['rating'], 2)

    def test_fail_to_update_book(self):
        res = self.client().patch('/books/5')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "bad request")

    def test_fail_to_delete_book(self):
        res = self.client().delete('/books/1000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['message'], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()