import json
import requests

from _default_paths.paths import paths


class APIConfig:
    '''
    Configuration class for setting base path and host.
    Runs methods that set up access tokens, includes auth body.
    '''

    def __init__(self):
        self.__headers_bearer = None
        self.__token_params = None

    with open(paths['config'] + "token.json", "r", encoding="utf-8") as f:
        token_params = json.load(f)

    with open(paths['config'] + "api_url.txt", "r", encoding='utf-8') as f:
        host_url = f.read()

    with open(paths['config'] + "POST_register", 'r', encoding="utf-8") as f:  # Example of JSON request
        auth_body = json.load(f)

    def setup_function(self):
        """
        Set token, save to globals.
        :return:
        """
        print("Running setup.")
        url_method = "registration-validations/auth/multi_step/start"
        response = requests.post(self.host_url + url_method, json=self.auth_body)
        json_response = json.loads(response.text)
        self.token_params["token"] = json_response['data']['accessToken']
        with open(paths['config'] + "global_params.json", 'w', encoding='utf-8') as f:
            json.dump(self.token_params, f, indent=4)
            f.close()

    def setup_headers(self):
        """
        Set Header.
        :return:
        """
        with open(paths['config'] + "headers.json", "r", encoding='utf-8') as f:
            headers_bearer = json.load(f)
        headers_bearer["X-API-Auth"] = f"Bearer {self.token_params['token']}"
        with open(paths['config'] + "headers.json", "w", encoding='utf-8') as f:
            json.dump(f, headers_bearer, indent=4)
        self.__headers_bearer = headers_bearer
        return headers_bearer
