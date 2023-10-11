import json
import pytest
import requests

from framework.functionality.api.base.api_init import APIConfig


class AuthTest(APIConfig):

    def __init__(self):
        super().__init__()

    @pytest.mark.auth
    def test_auth_user_default(self):
        headers = self.setup_headers()
        self.setup_function()
        url_method = 'auth/'
        payload = {}
        response = requests.get(self.host_url + url_method, params=payload, headers=headers)
        json_response = json.loads(response.text)
        assert response.status_code == 200
        assert json_response['status'] == 'ok'
        assert len(json_response['data']['brands']) != 0
        return json_response
