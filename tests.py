import unittest
import random
import string
import pymongo

from urllib import request

import settings

def gen_user():
    return 'http://user-service/'+str(random.randint(1,9999999))

def gen_class():
    cl = {'code':''.join([random.choice(string.ascii_letters) for i in range(10)]),
        'name': ''.join([random.choice(string.ascii_letters) for i in range(7)]),
        'teacher': gen_user(),
        'students': [gen_user() for i in range(random.randint(10)]
        }
    return cl
def gen_data():
    return [gen_class() for i in range(20)]

SchoolTestCase(unittest.TestCase):
    def setUp(self):
        settings.COLLECTION='testclasses'
        import models
        self.data = gen_data()
        self.collection = models.classes

    def tearDown(self):
        settings.COLLECTION='classes'

    def test_post(self):
        for cl in data:
            resp = request.urlopen('http://127.0.0.1:5000/classes',
                bytes(cl, 'utf-8'))
            assert resp.code==201
            assert cl.find_one({'code':cl['code']}

    def test_get(self):
        for cl in data:
            resp = request.urlopen('http://127.0.0.1:5000/classes/'+cl['code'])
            assert resp.code==200
