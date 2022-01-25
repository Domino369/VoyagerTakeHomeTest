""" Utility to pull config """
import json
from pathlib import Path


class Config(object):
    """ Class of methods of pulling config data """

    def get_json(self, filename):
        """
        Get config jsons as dictionary

        :param filename: Json file to get
        :return: Json as a dictionary
        """
        root_dir = Path(__file__).parent.parent
        with open('{rootdir}/configs/{filename}.json'.format(rootdir=root_dir, filename=filename), 'r') as json_file:
            json_dictionary = json.load(json_file)

        # Return the configuration as a dictionary
        return json_dictionary
