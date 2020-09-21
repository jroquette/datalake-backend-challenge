"""
File of test
"""
import unittest
import requests_mock
from dump import Dump


class TestDump(unittest.TestCase):
    """
    Class of test Dump
    """

    def setUp(self):
        self.dump = Dump("input-dump-test.tar.xz")

    def test_make_database(self):
        """
        Test make data base
        """
        database_mock = """{"productId": "pid1613", "images": ["http://localhost:4567/images/122577.png"]}
{"productId": "pid7471", "images": ["http://localhost:4567/images/177204.png"]}
{"productId": "pid2436", "images": ["http://localhost:4567/images/67717.png"]}"""
        self.dump.make_database()
        self.assertAlmostEqual(self.dump.database, database_mock)

    @requests_mock.Mocker(kw='mock')
    def test_validate_images(self, **kwargs):
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/1.png', status_code=200)
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/2.png', status_code=200)

        product_mock = """{
            'productId': '123',
            'images': ['http://localhost:4567/images/1.png', 'http://localhost:4567/images/2.png']
        }"""
        product = self.dump.validate_images(product_mock)
        self.assertEqual(product, eval(product_mock))

    @requests_mock.Mocker(kw='mock')
    def test_validate_images_one_invalid(self, **kwargs):
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/1.png', status_code=200)
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/2.png', status_code=400)

        product_mock = """{
                'productId': '123',
                'images': ['http://localhost:4567/images/1.png', 'http://localhost:4567/images/2.png']
                }"""

        product_expected = """{
                        'productId': '123',
                        'images': ['http://localhost:4567/images/1.png']
                        }"""
        product = self.dump.validate_images(product_mock)
        self.assertEqual(product, eval(product_expected))

    @requests_mock.Mocker(kw='mock')
    def test_validate_images_more_three(self, **kwargs):
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/1.png', status_code=200)
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/2.png', status_code=200)
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/3.png', status_code=200)
        kwargs['mock'].register_uri('GET', 'http://localhost:4567/images/4.png', status_code=200)

        product_mock = """{
                    'productId': '123',
                    'images': ['http://localhost:4567/images/1.png', 'http://localhost:4567/images/2.png', 
                    'http://localhost:4567/images/3.png', 'http://localhost:4567/images/4.png']
                     }"""

        product_expected = """{
                            'productId': '123',
                            'images': ['http://localhost:4567/images/1.png', 'http://localhost:4567/images/2.png', 
                            'http://localhost:4567/images/3.png']
                            }"""
        product = self.dump.validate_images(product_mock)
        self.assertEqual(product, eval(product_expected))


if __name__ == '__main__':
    unittest.main()
