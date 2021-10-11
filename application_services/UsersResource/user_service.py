from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as d_service
from database_services.RDBService import RDBService

class UserResource(BaseRDBApplicationResource):

    db_name, table_name = 'UserAddressDB', 'User' # TODO: replace with get_data_resource_info()

    def __init__(self):
        super().__init__()

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'e6156_hw0', 'users'

    @classmethod
    def get_users(cls, user_id=None):
        template = {'ID': user_id} if user_id else None
        result = RDBService.find_by_template(cls.db_name, cls.table_name, template, None)
        return result
    
    @classmethod
    def create_user(cls, data):
        RDBService.create(cls.db_name, cls.table_name, data)
        return "Successfully created user!"

    @classmethod
    def update_user(cls, user_id, data):
        template = {'ID': user_id}
        RDBService.update(cls.db_name, cls.table_name, template, data)
        return "Successfully updated user!"

    @classmethod
    def delete_user(cls, user_id):
        template = {'ID': user_id}
        RDBService.delete(cls.db_name, cls.table_name, template)
        return "Successfully deleted user!"
    