"""Test cases for module auth"""

import json
import unittest

from mixer.backend.flask import mixer

from flexbi import db
from flexbi.models import VerificationCode, User
from tests.base_tests import AuthTestCase


class SendVerificationCodeTest(AuthTestCase):
    URI = '/auth/verification_code'

    def test_send_verification_code(self):
        response = self.client.post(
            self.URI,
            base_url=self.base_url,
            data=json.dumps({
                'email': self.email,
                'code_type': 0
            }
            ),
            headers=self.headers
        )
        self.assertEqual(response.json, dict(success=True))


class UserRegisterTest(AuthTestCase):
    URI = '/auth/register'

    def setUp(self):
        super(UserRegisterTest, self).setUp()
        self.set_verification_code(self.verification_code)

    def set_verification_code(self, code):
        session = db.session

        v_code_obj = VerificationCode.query.filter_by(
            email=self.email, company_id=self.company_id).first()
        if v_code_obj is not None:
            v_code_obj.verification_code = code
        else:
            v_code_obj = VerificationCode(
                email=self.email,
                code=code,
                company_id=self.company_id
            )
        session.add(v_code_obj)
        session.commit()

    def test_user_register_success(self):
        response = self.client.post(
            self.URI,
            base_url=self.base_url,
            data=json.dumps({
                'email': self.email,
                'name': self.name,
                'password': self.password,
                'password_confirm': self.password_confirm,
                'code': self.verification_code
            }),
            headers=self.headers
        )
        self.assertEqual(response.json, dict(success=True))

    def test_user_register_fail(self):
        verification_code = '54321'

        response = self.client.post(
            self.URI,
            base_url=self.base_url,
            data=json.dumps({
                'email': self.email,
                'name': self.name,
                'password': self.password,
                'password_confirm': self.password_confirm,
                'code': verification_code
            }),
            headers=self.headers
        )
        self.assertNotEqual(response.json, dict(success=True))


class UserResetPasswordTest(AuthTestCase):
    URI = '/auth/reset_password'

    def setUp(self):
        super(UserResetPasswordTest, self).setUp()
        self.set_verification_code(self.verification_code)
        self.user = mixer.blend(
            User,
            name='test user',
            email=self.email,
            password=self.password,
            company_id=self.company_id
        )

    def test_reset_password_success(self):
        password = '1234567'
        password_confirm = '1234567'

        user = User.query.filter_by(
            email=self.email, company_id=self.company_id).first()
        assert user is not None

        response = self.client.post(self.URI,
                                    base_url=self.base_url,
                                    data=json.dumps({
                                        'email': self.email,
                                        'password': password,
                                        'password_confirm': password_confirm,
                                        'code': self.verification_code
                                    }),
                                    headers=self.headers)
        self.assertEqual(response.json, dict(success=True))

    def set_verification_code(self, code):
        session = db.session

        v_code_obj = VerificationCode.query.filter_by(
            email=self.email, company_id=self.company_id).first()
        if v_code_obj is not None:
            v_code_obj.verification_code = code
        else:
            v_code_obj = VerificationCode(
                email=self.email,
                code=code,
                company_id=self.company_id
            )
        session.add(v_code_obj)
        session.commit()

    def test_reset_password_fail(self):
        password = '12345'
        password_confirm = '12345'

        user = User.query.filter_by(
            email=self.email, company_id=self.company_id).first()
        assert user is not None

        response = self.client.post(
            self.URI,
            base_url=self.base_url,
            data=json.dumps({
                'email': self.email,
                'password': password,
                'password_confirm': password_confirm,
                'code': self.verification_code
            }),
            headers=self.headers
        )
        self.assertNotEqual(response.json, dict(success=True))


class LoginTest(AuthTestCase):
    URI = '/auth/login'

    def setUp(self):
        super(LoginTest, self).setUp()
        self.user = mixer.blend(
            User,
            name='test user',
            email=self.email,
            password=self.password,
            company_id=self.company_id
        )

    def test_login_success(self):
        response = self.client.post(
            self.URI,
            data=json.dumps({
                'username': self.email,
                'password': self.password
            }),
            headers=self.headers
        )
        self.assert200(response)

    def test_login_incorrect_password_fail(self):
        response = self.client.post(
            self.URI,
            data=json.dumps({
                'username': self.email,
                'password': 'fake_password'
            }),
            headers=self.headers
        )
        self.assert401(response)

    def test_login_incorrect_username_fail(self):
        response = self.client.post(
            self.URI,
            data=json.dumps({
                'username': 'fake_email@fake.com',
                'password': self.password
            }),
            headers=self.headers
        )
        self.assert401(response)


if __name__ == '__main__':
    unittest.main()
