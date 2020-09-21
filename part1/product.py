"""File Product"""
from hashlib import md5

from datetime import datetime


class Product_Struct:
    """Class of Product"""
    def __init__(self, product_id, name):
        """
        Constructor of product class

        :param product_id: id of product
        :param name: name of product
        """
        self.product = {"id": product_id,
                       "name": name,
                       "hash": md5(f"{product_id}|{name}".encode('utf-8')).hexdigest(),
                       "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
