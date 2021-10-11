from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


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

@app.route('/users', methods = ['GET'])
@app.route('/users/<user_id>', methods = ['GET'])
def get_users(user_id=None):
    # res = UserResource.get_by_template(None)
    res = UserResource.get_users(user_id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users', methods = ['POST'])
def create_user():
    data = request.get_json()
    res = UserResource.create_user(data)
    return res

@app.route('/users/<user_id>', methods = ['PUT'])
def update_user(user_id):
    data = request.get_json()
    res = UserResource.update_user(user_id, data)
    return res

@app.route('/users/<user_id>', methods = ['DELETE'])
def delete_user(user_id):
    res = UserResource.delete_user(user_id)
    return res


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
