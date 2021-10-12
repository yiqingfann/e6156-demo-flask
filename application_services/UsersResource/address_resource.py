from application_services.BaseApplicationResource import BaseApplicationResource
from database_services.RDBService import RDBService


class AddressResource(BaseApplicationResource):

    db_name = "UserAddressDB"
    table_name = "Address"

    def __init__(self):
        super().__init__()

    @classmethod
    def create(cls, new_address):
        pass

    @classmethod
    def get_links(self, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return cls.db_name, cls.table_name

    @classmethod
    def create_address(cls, data):
        res, id = RDBService.create(cls.db_name, cls.table_name, data)
        msg = "Successfully created address!"
        return msg, id
    
    @classmethod
    def get_addresses(cls, address_id=None):
        template = {'ID': address_id} if address_id else None
        result = RDBService.find_by_template(cls.db_name, cls.table_name, template, None)
        return result
    
    @classmethod
    def update_address(cls, address_id, data):
        template = {'ID': address_id}
        RDBService.update(cls.db_name, cls.table_name, template, data)
        return "Successfully updated address!"
    
    @classmethod
    def delete_address(cls, address_id):
        template = {'ID': address_id}
        RDBService.delete(cls.db_name, cls.table_name, template)
        return "Successfully deleted address!"
    