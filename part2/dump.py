"""
Dump Project
"""
import codecs
import tarfile
import json
import sys
import requests
import concurrent.futures


class Dump:
    def __init__(self, dump_file):
        """Construct of Dump Class"""
        self.dump_file = dump_file
        self.database = None

    def make_database(self):
        """
        Create a database from tar file and set in class
        """
        my_tar = tarfile.open(self.dump_file)
        utf8reader = codecs.getreader('utf-8')
        file = my_tar.extractfile(my_tar.getmembers()[0])
        str_database = utf8reader(file).read()
        database = {}
        for str_data in str_database.split('\n'):
            try:
                data = eval(str_data)
                product_id = data.get('productId', None)
                if database.get(product_id):
                    database[product_id].append(data.get('image'))
                else:
                    database[product_id] = [data.get('image')]
            except:
                continue
        self.database = self.formart_database(database)

    def export_database(self, filename="dump"):
        """Export data base with validate images"""
        if self.database is None:
            print("Não foi possivel exportar a base de dados, pois não há dados")
            sys.exit(-1)
        dump = open(f"{filename}.json", "w+")
        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            future_to_url = {executor.submit(self.validate_images, product): product for product in
                             self.database.split('\n')}
            for future in concurrent.futures.as_completed(future_to_url):
                data = future.result()
                dump.write(json.dumps(data) + '\n')

    def formart_database(self, database):
        """
        Save database in json format
        """
        data = ''
        index = 1
        for product in map(self.product_struct, database.keys(), database.values()):
            if index == len(database.keys()):
                data = data + json.dumps(product)
                continue
            data = data + json.dumps(product) + '\n'
            index = index + 1
        return data

    @staticmethod
    def validate_images(product):
        """
        Validate if images from a pid has status code 200

        :param product: product with pid and urls images
        :return: product with max 3 images with status code 200
        """
        images_ok = []
        try:
            product = eval(product)
            for url in product.get('images'):
                if requests.get(url).status_code == 200:
                    images_ok.append(url)
                if len(images_ok) >= 3:
                    break
            product['images'] = images_ok
        except:
            pass
        return product

    @staticmethod
    def product_struct(pid, urls):
        """
        struct of product
        :param pid: pid code
        :param urls: urls images
        :return: retrun dict of product
        """
        data = {
            'productId': pid,
            'images': urls
        }
        return data
