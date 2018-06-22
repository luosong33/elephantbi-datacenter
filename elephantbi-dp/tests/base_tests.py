import json
from copy import deepcopy

from flask_testing import TestCase
from mixer.backend.flask import mixer
from werkzeug.security import generate_password_hash

from flexbi import create_app, db
from flexbi.configuration import get_config
from flexbi.logger import config_logger
from flexbi.models import User, Company

logger = config_logger(__name__, 'info', 'test.log')


@mixer.middleware(User)
def encrypt_password(user):
    user.password = generate_password_hash(user.password)
    return user


class FlexBIBaseTestCase(TestCase):

    def create_app(self):
        app = create_app(get_config('test'))

        mixer.init_app(app)

        return app

    def setUp(self):
        db.create_all()
        self.auth_base_url = 'http://flexceed.com:5000'
        self.base_url = 'http://localhost.flexceed.com:5000'
        self.headers = [
            ('Content-Type', 'application/json')
        ]

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def login(self, username, password):
        response = self.client.post(
            '/auth/login',
            base_url=self.auth_base_url,
            data=json.dumps({
                'username': username,
                'password': password
            }),
            headers=self.headers
        )

        access_token = response.json.get('access_token')

        return access_token


class AuthTestCase(FlexBIBaseTestCase):

    def setUp(self):
        super(AuthTestCase, self).setUp()

        # Create a company
        self.company = mixer.blend(
            Company,
            domain='localhost'
        )
        self.company_id = self.company.id

        # Pre-defined user info
        self.email = 'dev@visionpsn.com'
        self.name = 'dev'
        self.password = 'password123'
        self.password_confirm = 'password123'
        self.verification_code = '5432'


class UserTestCase(FlexBIBaseTestCase):
    # TODO
    pass


class AdminTestCase(FlexBIBaseTestCase):

    def setUp(self):
        super(AdminTestCase, self).setUp()

        # Create a company
        self.company = mixer.blend(
            Company,
            domain='localhost'
        )
        self.company_id = self.company.id

        # Create an Admin user (is_admin=1), and a Member user (is_admin=0)
        self.admin_email = 'admin@flexbi.com'
        self.member_email = 'member@flexbi.com'
        self.admin_pwd = 'admin_fake_pwd'
        self.member_pwd = 'member_fake_pwd'
        self.admin = mixer.blend(
            User,
            is_admin=1,
            name='Admin',
            email=self.admin_email,
            password=self.admin_pwd,
            company_id=self.company_id
        )
        self.member = mixer.blend(
            User,
            is_admin=0,
            name='John',
            email=self.member_email,
            password=self.member_pwd,
            company_id=self.company_id
        )
        self.admin_token = self.login(self.admin.email, self.admin_pwd)
        self.member_token = self.login(self.member.email, self.member_pwd)

    def admin_headers(self):
        headers = deepcopy(self.headers)
        headers.append(('Authorization', 'jwt %s' % self.admin_token))

        return headers

    def member_headers(self):
        headers = deepcopy(self.headers)
        headers.append(('Authorization', 'jwt %s' % self.member_token))

        return headers
