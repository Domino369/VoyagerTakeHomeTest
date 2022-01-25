""" Tool to execute api requests """
from requests.api import get


class ApiRequest(object):
    """ Class with static methods of executing api requests """

    # variables
    __auth = None

    def __init__(self):
        """ Constructor """
        pass

    def get(self, url, headers=None, payload=None, json=None, timeout=5):
        """
        Get api request method

        :param url: URL to call
        :param headers: Headers to define the endpoint
        :param payload: Payload to send the endpoint
        :param json: Json to send the endpoint
        :param timeout: Timeout for endpoint call
        :return response: Raw response from the endpoint
        """
        response = get(url, headers=headers, data=payload, json=json, auth=self.__auth, timeout=timeout)
        return response
