"""
File of test
"""
import unittest


from app import app


class TestDump(unittest.TestCase):
    """
    Class of test Dump
    """
    def setUp(self):
        self.application = app.test_client()

    def test_save_product_more_10_minutes(self):
        """Test add product in database with more 10 minutes of last update"""
        old_data = eval(self.application.get('/products').data)
        response = self.application.post('/save_products', json={
            'id': '1', 'name': 'sofa'
        })
        new_data = eval(self.application.get('/products').data)
        self.assertEqual(response.status, "200 OK")
        self.assertEqual(len(old_data), len(new_data))

    def test_save_product_less_10_minutes(self):
        """Test add product in database with more 10 minutes of less update"""
        old_data = eval(self.application.get('/products').data)
        response_1 = self.application.post('/save_products', json={
            'id': '5', 'name': 'chave'
        })
        self.assertEqual(response_1.status, "200 OK")
        new_data = eval(self.application.get('/products').data)
        self.assertNotEqual(len(old_data), len(new_data))
        old_data = new_data

        response_2 = self.application.post('/save_products', json={
            'id': '5', 'name': 'chave'
        })
        self.assertEqual(response_2.status, "404 NOT FOUND")
        new_data = eval(self.application.get('/products').data)
        self.assertEqual(len(old_data), len(new_data))

    def test_save_product_id_exists(self):
        """Test add product in database with id exists"""
        old_data = eval(self.application.get('/products').data)
        response = self.application.post('/save_products', json={
            'id': '1', 'name': 'mesa'
        })
        new_data = eval(self.application.get('/products').data)
        self.assertEqual(eval(response.data), {'error': 'id already exists'})
        self.assertEqual(response.status, "404 NOT FOUND")
        self.assertEqual(len(old_data), len(new_data))

    def test_add_new_product(self):
        """Test add new product in database"""
        old_data = eval(self.application.get('/products').data)
        response = self.application.post('/save_products', json={
            'id': '3', 'name': 'mesa'
        })
        new_data = eval(self.application.get('/products').data)
        self.assertEqual(response.status, "200 OK")
        self.assertNotEqual(len(old_data), len(new_data))


if __name__ == '__main__':
    unittest.main()
