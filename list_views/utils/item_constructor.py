import json
import time

from list_views.utils.constants import *
from list_views.utils import exclude_keys

class ItemConstructor():

    def __init__(self, details):
        self.json_details = details
        self.partition_key = ""
        self.primary_key = {}
        self.sort_key = ""

    def itemize(self, only_partition_key=False):
        if self.__validate_keys():
            self.primary_key = {
                PARTITION_KEY: self.__build_partition_key()
            }

            if not only_partition_key:
                self.primary_key[SORT_KEY] = self.__build_sort_key()

            self.json_details.update(self.primary_key)
        else:
            self.json_details = {}

    def get_attributes_values_expression(self):
        timestamp = int(time.time() * 1000)
        details = self.__json_details_without_partition_key()
        expr = {}

        for key in details.keys():
            expr[':%s' % key] = details[key]

        expr[':updatedAt'] = str(timestamp)

        return expr

    def get_update_expression(self):
        details = self.__json_details_without_partition_key()
        expr = ['updatedAt = :updatedAt']

        for key     in details.keys():
            str = '%s = :%s' % (key, key)
            expr.append(str)

        return 'set ' + ','.join(expr)

    '''
    Only enforcing presence of partition_key
    '''
    def __validate_keys(self):
        keys = [
            'application_id',
            'section_id'
        ]

        for key in keys:
            if self.json_details.get(key) is None:
                return False

        return True

    def __build_partition_key(self):
        self.partition_key =  self.__join_keys('application_id', 'section_id')

        return self.partition_key

    def __build_sort_key(self):
        self.sort_key = self.__join_keys('listing_type', 'listing_id')

        return self.sort_key

    def __join_keys(self, *args):
        keys = []

        for k in args:
            keys.append(self.json_details.get(k))

        return '_'.join(keys)

    def __json_details_without_partition_key(self):
        excluded_keys = [
            'application_id',
            'section_id',
            'listing_type',
            'listing_id',
            PARTITION_KEY,
            SORT_KEY
        ]

        return exclude_keys(excluded_keys, self.json_details)
