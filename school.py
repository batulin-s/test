import re
import copy

from bson.objectid import ObjectId
from flask import request, json
from flask import Flask


import pymongo
from pymongo.errors import *

from models import *

app=Flask(__name__)


@app.errorhandler(DuplicateKeyError)
def duperror(error):
    print(error.details)
    return error.details['errmsg'].split('classes.$')[1], 406

@app.errorhandler(MyValidationError)
def valerror(error):
    print(error.message)
    return json.dumps(error.to_dict()), 406



@app.route('/classes/<class_code>', methods=['GET', 'PUT', 'DELETE'])
def get_class(class_code):
    if request.method == 'GET':
        cl = classes.find_one({'code':class_code})
        return cl
    elif request.method == 'PUT':
        class_data = request.get_json(force=True)
        print(class_data)
        if 'code' in class_data.keys():
            raise MyValidationError("code couldn't be changed")
        classes.update_one({'code':class_code}, {'$set':class_data})
        return 'Updated', 202
    elif request.method =='DELETE':
        classes.delete_one({'code':class_code})
        return 'Deleted', 202

@app.route('/classes', methods=['GET', 'POST'])
def post_class():
    if request.method == 'POST':
        class_data = request.get_json(force=True)
        is_valid = class_validator(class_data)
        if is_valid:
            class_id = classes.insert_one(class_data).inserted_id
        return 'Created', 201
    if request.method == 'GET':
        if request.args:
            if 'student' in request.args.keys():
                n_args = dict(request.args)
                n_args['students'] = n_args['student']
                n_args.pop('student')
                n_args = {i:j[0] for i, j in n_args.items()}
            else:
                n_args = request.args
            print(n_args)
            result = classes.find(n_args)
        else: result = classes.find()
        res=[]
        for r in result:
            r['_id'] = str(r['_id'])
            res.append(r)
        return json.dumps(res)
