import re


import pymongo


from settings import *

client=pymongo.MongoClient() 
db = client[DB]
db_validator = {'$and': [{'name': {'$type': 'string'}}, 
    {'code': {'$regex': '^[A-Za-z]{10}'}}, 
    {'teacher': {'$regex': '^http:\\/\\/user-service\\/.*'}}, 
    {'students': {'$elemMatch': {'$regex': '^http:\\/\\/user-service\\/'}}}]} 
 
if COLLECTION not in db.collection_names(): 
    db.create_collection(COLLECTION) 
    classes = db[COLLECTION] 
    classes.create_index([("name", pymongo.ASCENDING)], unique=True) 
    classes.create_index([("code", pymongo.ASCENDING)], unique=True) 
else: 
    classes = db[COLLECTION]
 

class MyValidationError(Exception):
    status_code=406
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message=message
        self.payload = payload
        if status_code:
            self.status_code = status_code
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

validd={'name':lambda name: isinstance(name, str),
    'code': lambda code: re.match('^[A-Za-z]{10}$', code),
    'user': lambda teach: re.match('^http:\/\/user-service\/.*', teach),
    }


def class_validator(class_data):
    if not validd['name'](class_data.get('name', None)):
        raise MyValidationError("The name couldn't be blank")
    if not validd['code'](class_data.get('code','')):
        raise MyValidationError("The code should contains excactly 10 letters")
    if 'teacher' in class_data.keys() and not validd['user'](class_data['teacher']):
        raise MyValidationError("teacher field should be formed as http://user-service/1245 link")
    if 'students' in class_data.keys():
        for st in class_data['students']:
            if not validd['user'](st):
                raise MyValidationError("student field should be formed as http://user-service/1245 link")
    return True



'''

class BaseField():
    _name=None
    unique=False
    required=False
    regexp=None
    def __init__(self, **kw):
        if 'unique' in kw.keys():
            self.unique = kw['unique']
        if 'required' in kw.keys():
            self.required = kw['required']
        if 'regexp' in kw.keys():
            self.regexp = kw['regexp']

    def validate(self, field):
        if not field and not self.required:
            return True
        if field and self.regexp:
            if re.match(self.regexp, field):
                return True
        if field and not self.regexp:
            return True
        return False


class ListField():
    _name=None
    def __init__(self, base_field):
        self.base_field=base_field
    def validate(self, listfield):
        for i in listfield:
            assert self.base_field.validate(i), True


class MyClass():
    name = BaseField(unique=True, required=True)
    code = BaseField(unique=True, required=True, regexp='^[A-Za-z]{10}$')
    teacher = BaseField(regexp='^http:\/\/user-service\/.*')
    students = ListField(BaseField(regexp='^http:\/\/user-service\/.*'))


myclass=MyClass()
'''
