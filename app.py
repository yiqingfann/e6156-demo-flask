from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from application_services.UsersResource.address_resource import AddressResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

# ------------------- routing functions -------------------

@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'

@app.route('/users', methods = ['POST'])
def create_user():
    user_data = request.get_json()
    try:
        msg, id = create_user_helper(user_data)
        rsp = Response(msg, status=201)
        rsp.headers['location'] = f"/users/{id}"
    except:
        rsp = Response("Integrity error, create failed.", status=422)
    return rsp

@app.route('/users', methods = ['GET'])
@app.route('/users/<user_id>', methods = ['GET'])
def get_users(user_id=None):
    pagination = {}
    pagination['offset'] = request.args.get('offset')
    pagination['limit'] = request.args.get('limit')
    fields = request.args.get('fields')
    fields = fields.split(',') if fields else None
    res = UserResource.get_users(user_id, pagination, fields)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users/<user_id>', methods = ['PUT'])
def update_user(user_id):
    user_data = request.get_json()
    try:
        msg = update_user_helper(user_id, user_data)
        rsp = Response(msg, status=200)
    except Exception as e:
        rsp = Response("Update failed because of bad data", status=400)
    return rsp

@app.route('/users/<user_id>', methods = ['DELETE'])
def delete_user(user_id):
    res = UserResource.delete_user(user_id)
    rsp = Response(status=204)
    return rsp

@app.route('/users/<user_id>/address', methods = ['GET'])
def get_user_address(user_id):
    res = UserResource.get_users(user_id)
    rsp = get_addresses(res[0]['addressID'])
    return rsp

@app.route('/users/<user_id>/address', methods = ['POST'])
def create_address_for_user(user_id):
    addr_data = request.get_json()
    msg, addr_id = AddressResource.create_address(addr_data)

    user_data = {'addressID': addr_id}
    UserResource.update_user(user_id, user_data)

    rsp = Response("Successfully created address for user!", status=201)
    rsp.headers['location'] = f"/addresses/{addr_id}"

    return rsp

@app.route('/addresses', methods = ['POST'])
def create_address():
    data = request.get_json()
    msg, id = AddressResource.create_address(data)
    rsp = Response(msg, status=201)
    rsp.headers['location'] = f"/addresses/{id}"
    return rsp

@app.route('/addresses', methods = ['GET'])
@app.route('/addresses/<address_id>', methods = ['GET'])
def get_addresses(address_id=None):
    res = AddressResource.get_addresses(address_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/addresses/<address_id>', methods = ['PUT'])
def update_address(address_id):
    data = request.get_json()
    msg = AddressResource.update_address(address_id, data)
    rsp = Response(msg, status=200)
    return rsp

@app.route('/addresses/<address_id>', methods = ['DELETE'])
def delete_address(address_id):
    res = AddressResource.delete_address(address_id)
    rsp = Response(status=204)
    return rsp

@app.route('/addresses/<address_id>/users', methods = ['GET'])
def get_all_users_under_address(address_id):
    template = {'addressID': address_id}
    res = UserResource.get_by_template(template)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/addresses/<address_id>/users', methods = ['POST'])
def create_user_under_address(address_id):
    user_data = request.get_json()
    msg, user_id = create_user_helper(user_data)

    user_data = {'addressID': address_id}
    msg = update_user_helper(user_id, user_data)
    
    return "Successfully created user under address!"

# ------------------- helper functions -------------------

def create_user_helper(user_data):
    msg, user_id = UserResource.create_user(user_data)
    return msg, user_id

def update_user_helper(user_id, user_data):
    msg = UserResource.update_user(user_id, user_data)
    return msg

# ------------------- main function -------------------

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)







# @app.route('/imdb/artists/<prefix>')
# def get_artists_by_prefix(prefix):
#     res = IMDBArtistResource.get_by_name_prefix(prefix)
#     rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     return rsp

# @app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
# def get_by_prefix(db_schema, table_name, column_name, prefix):
#     res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
#     rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
#     return rsp