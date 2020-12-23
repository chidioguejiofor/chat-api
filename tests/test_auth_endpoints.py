import json

from api.utils.messages.errors import ALREADY_EXISTS, INVALID_INPUT, NOT_FOUND
from api.utils.token_helpers import decode_token

LOGIN_URL = '/api/login'
REGISTER_URL = '/api/register'


class TestRegisterEndpoint:
    def test_user_should_be_registered_when_data_is_valid(self, client, init_db):
        api_data = {
            "email": "email@email.com",
            "password": "password",
            "username": "username"
        }

        response = client.post(REGISTER_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 201
        assert response_body['username'] == api_data['username']
        assert response_body['email'] == api_data['email']
        assert 'data' not in response_body
        assert 'id' in response_body

    def test_should_return_409_when_email_already_exists(self, client,init_db,  saved_user_model):
        api_data = {
            "email": saved_user_model.email,
            "password": "password",
            "username": 'thisusername_is_valid'
        }

        response = client.post(REGISTER_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 409
        assert response_body['message'] ==  ALREADY_EXISTS.format('username or email')

    def test_should_return_409_when_username_already_exists(self, client,init_db,  saved_user_model):
        api_data = {
            "email": 'newemailthathasnotbeenused@email.com',
            "password": "password",
            "username":  saved_user_model.username
        }

        response = client.post(REGISTER_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 409
        assert response_body['message'] ==  ALREADY_EXISTS.format('username or email')

    def test_should_return_400_when_no_data_is_provided(self, client,init_db,  saved_user_model):
        api_data = {}

        response = client.post(REGISTER_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 400
        errors = response_body['errors']
        assert errors['password'][0] == 'Missing data for required field.'
        assert errors['username'][0] == 'Missing data for required field.'
        assert errors['email'][0] == 'Missing data for required field.'
        assert response_body['message'] ==  INVALID_INPUT


class TestLoginEndpoint:
    def test_login_when_data_is_valid(self, client,  init_db, saved_user_model):
        user_password = 'this-is-the-password1234'
        saved_user_model.password = user_password
        saved_user_model.update()
        api_data = {
            "email": saved_user_model.email,
            "password": user_password,
        }

        response = client.post(LOGIN_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 200
        assert response_body['email'] == saved_user_model.email
        assert response_body['id'] == saved_user_model.id
        assert 'token' in response_body
        token = response_body['token']
        token_data = decode_token(token)
        assert token_data['data']['email'] == saved_user_model.email
        assert token_data['data']['username'] == saved_user_model.username
        assert token_data['data']['id'] == saved_user_model.id

    def test_should_return_a_404_when_password_is_not_invalid(self, client, init_db, saved_user_model):
        api_data = {
            "email": saved_user_model.email,
            "password": 'user_password',
        }

        response = client.post(LOGIN_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 404
        assert response_body['message'] == NOT_FOUND.format('Credentials')

    def test_should_return_a_404_when_email_is_not_found(self, client, init_db, saved_user_model):
        user_password = 'this-is-the-password1234'
        saved_user_model.password = user_password
        saved_user_model.update()
        api_data = {
            "email": 'missing@email.com',
            "password": user_password,
        }

        response = client.post(LOGIN_URL,
                               data=json.dumps(api_data),
                               content_type="application/json")
        response_body = json.loads(response.data)

        assert response.status_code == 404
        assert response_body['message'] == NOT_FOUND.format('Credentials')




