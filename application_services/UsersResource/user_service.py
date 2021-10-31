from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as d_service
from database_services.RDBService import RDBService

class UserResource(BaseRDBApplicationResource):

    # TODO: replace with get_data_resource_info() ?
    db_name = 'UserAddressDB' 
    table_name = 'User'

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return cls.db_name, cls.table_name

    @classmethod
    def create_user(cls, data):
        res, id = RDBService.create(cls.db_name, cls.table_name, data)
        msg = "Successfully created user!"
        return msg, id
    
    @classmethod
    def get_users(cls, user_id=None, pagination=None, fields=None):
        template = {'userID': user_id} if user_id else None
        data = RDBService.find_by_template_and_pagination(cls.db_name, cls.table_name, template, pagination, fields)
        users = {}
        users['data'] = data
        users['links'] = [
            {'rel': 'prev', 'href': f"/users?limit={pagination['limit']}&offset={int(pagination['offset'])-int(pagination['limit'])}"},
            {'rel': 'self', 'href': f"/users?limit={pagination['limit']}&offset={pagination['offset']}"},
            {'rel': 'prev', 'href': f"/users?limit={pagination['limit']}&offset={int(pagination['offset'])+int(pagination['limit'])}"},
        ]

        for i, user in enumerate(users['data']):
            links = [
                {'rel': "self", "href": f"/users/{user['userID']}"},
                {'rel': "address", "href": f"/addresses/{user['addressID']}"}
            ]
            if fields:
                users['data'][i] = {field: user[field] for field in fields}
            users['data'][i]['links'] = links
            
        return users

    @classmethod
    def update_user(cls, user_id, data):
        template = {'userID': user_id}
        if "email" in data and "@" not in data['email']:
            raise Exception('Invalid email')
        RDBService.update(cls.db_name, cls.table_name, template, data)
        return "Successfully updated user!"

    @classmethod
    def delete_user(cls, user_id):
        template = {'userID': user_id}
        RDBService.delete(cls.db_name, cls.table_name, template)
        return "Successfully deleted user!"
    