""" Utility used to execute queries against /repos """
from utilities.apirequest import ApiRequest
from utilities.config import Config


class Repos(object):
    """ Class used to execute queries against /repos """

    def __init__(self, user):
        """ Constructor """
        # apis
        self.__request_api = ApiRequest()

        # variables
        self.__headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        config = Config()
        urls = config.get_json("urls")
        users = config.get_json("users")
        self.__url = urls['github'] + "users/" + users[user] + "/repos"

    def execute(self, repo_type="owner", sort="full_name", direction="asc", per_page=30, page=1, timeout=5):
        """
        /repos get api request method

        :param repo_type: Type of repo, can be all, owner, or member
        :param sort: Order of repos returned, can be created, updated, pushed, or full_name
        :param direction: Direction of order, can be asc or desc
        :param per_page: Results per page, with max of 100
        :param page: Number of pages to return
        :param timeout: Timeout for endpoint call
        :return response: Raw response from the endpoint
        """
        request = dict(
            type=repo_type,
            sort=sort,
            direction=direction,
            per_page=per_page,
            page=page
        )

        response = self.__request_api.get(self.__url, self.__headers, payload=request, timeout=timeout)
        return response
