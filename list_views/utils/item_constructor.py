import json

from list_views.utils.constants import *

class ItemConstructor():

    def __init__(self, details):
        self.json_details = details
        self.partition_key = ""
        self.primary_key = {}
        self.sort_key = ""

    def itemize(self):
        if self.__validate_keys():
            self.primary_key = {
                PARTITION_KEY: self.__build_partition_key(),
                SORT_KEY: self.__build_sort_key()
            }

            self.json_details.update(self.primary_key)
        else:
            self.json_details = {}

    def __validate_keys(self):
        keys = [
            'application_id',
            'section_id',
            'listing_type',
            'listing_id'
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
