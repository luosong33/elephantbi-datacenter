"""Test cases for module admin.group"""
import json
import unittest

from mixer.backend.flask import mixer

from flexbi.ma_schemas import UserSchema
from flexbi.models import Group, User
from tests.base_tests import AdminTestCase


class GroupsTest(AdminTestCase):
    URI = '/admin/groups'

    def test_groups_get_401(self):
        """Non-admin user cannot access the groups list"""
        # Request without access_token
        get_resp1 = self.client.get(self.URI, base_url=self.base_url)
        self.assert401(get_resp1)

        post_resp1 = self.client.post(self.URI, base_url=self.base_url,
                                      headers=self.headers)
        self.assert401(post_resp1)

        # Request with non-admin access_token
        get_resp2 = self.client.get(self.URI, base_url=self.base_url,
                                    headers=self.member_headers())
        self.assert401(get_resp2)

        post_resp2 = self.client.post(self.URI, base_url=self.base_url,
                                      headers=self.member_headers())
        self.assert401(post_resp2)

    def test_groups_get_empty(self):
        """Getting groups list when there isn't any groups yet"""
        response = self.client.get(self.URI, base_url=self.base_url,
                                   headers=self.admin_headers())

        self.assertEqual(response.json, [])

    def test_groups_get_list(self):
        """Getting groups list"""
        # Add some groups
        expected_groups = mixer.cycle(5).blend(Group,
                                               name=mixer.sequence('group_{0}'),
                                               company_id=self.company_id)
        expected_group_names = {group.name for group in expected_groups}

        response = self.client.get(self.URI, base_url=self.base_url,
                                   headers=self.admin_headers())
        actual_groups = response.json
        actual_groups_names = {group['name'] for group in actual_groups}

        self.assertEqual(expected_group_names, actual_groups_names)

    def test_groups_post(self):
        """Add a new group"""
        expected_group_name = 'test_group_name'

        response = self.client.post(
            self.URI,
            base_url=self.base_url,
            headers=self.admin_headers(),
            data=json.dumps({
                'name': expected_group_name
            })
        )
        self.assert200(response)

        group_id = response.json.get('id')
        self.assertIsNotNone(group_id)

        actual_group = Group.query.filter_by(
            id=group_id, company_id=self.company_id).first()
        self.assertIsNotNone(actual_group)
        self.assertEqual(actual_group.name, expected_group_name)


class SingleGroupTest(AdminTestCase):
    URI = '/admin/group/%s'

    def test_single_group_401(self):
        # Add a group
        group = mixer.blend(Group)
        group_id = group.id

        uri = self.URI % group_id

        # Request without access_token
        put_resp1 = self.client.put(uri, base_url=self.base_url)
        self.assert401(put_resp1)

        delete_resp1 = self.client.delete(uri, base_url=self.base_url)
        self.assert401(delete_resp1)

        # Request with non-admin access_token
        put_resp2 = self.client.put(uri, base_url=self.base_url,
                                    headers=self.member_headers())
        self.assert401(put_resp2)

        delete_resp2 = self.client.delete(uri, base_url=self.base_url,
                                          headers=self.member_headers())
        self.assert401(delete_resp2)

    def test_single_group_put(self):
        # Add a group
        expected_group = mixer.blend(
            Group,
            name='test group name',
            company_id=self.company_id
        )
        group_id = expected_group.id
        uri = self.URI % group_id

        expected_group_name = 'new test group name'
        response = self.client.put(
            uri,
            headers=self.admin_headers(),
            base_url='http://localhost.flexceed.com:5000',
            data=json.dumps({
                'name': expected_group_name,
            })
        )
        self.assert200(response)

        # Actual group
        group_id = response.json.get('id')
        self.assertIsNotNone(group_id)

        group = Group.query.filter_by(
            id=group_id, company_id=self.company_id).first()
        self.assertIsNotNone(group)
        self.assertEqual(group.name, expected_group_name)

    def test_single_group_delete(self):
        # Add a group
        expected_group = mixer.blend(Group, name='test group name',
                                     company_id=self.company_id)
        group_id = expected_group.id
        uri = self.URI % group_id

        response = self.client.delete(uri, base_url=self.base_url,
                                      headers=self.admin_headers())
        self.assert200(response)

        # Actual group
        group_id = response.json.get('id')
        self.assertIsNotNone(group_id)

        group = Group.query.filter_by(
            id=group_id, company_id=self.company_id).first()
        self.assertIsNone(group)


class GroupUsersTest(AdminTestCase):
    URI = '/admin/group/%s/users'

    def test_group_users_401(self):
        group = mixer.blend(Group)
        group_id = group.id

        uri = self.URI % group_id

        # Request without access_token
        get_resp1 = self.client.get(uri, base_url=self.base_url)
        self.assert401(get_resp1)

        post_resp1 = self.client.post(uri, base_url=self.base_url)
        self.assert401(post_resp1)

        delete_resp1 = self.client.post(uri, base_url=self.base_url)
        self.assert401(delete_resp1)

        # Request with non-admin access_token
        get_resp2 = self.client.get(uri, base_url=self.base_url,
                                    headers=self.member_headers())
        self.assert401(get_resp2)

        post_resp2 = self.client.post(uri, base_url=self.base_url,
                                      headers=self.member_headers())
        self.assert401(post_resp2)

        delete_resp2 = self.client.post(uri, base_url=self.base_url,
                                        headers=self.member_headers())
        self.assert401(delete_resp2)

    def test_group_users_get_empty(self):
        group = mixer.blend(Group, company_id=self.company_id)
        uri = self.URI % group.id
        query = 'page=1&page_size=10'
        expected = {
            'meta': {
                'total_count': 0,
                'page_count': 0,
                'current_page': 1,
                'page_size': 10
            },
            'list': []
        }

        response = self.client.get(
            uri,
            base_url=self.base_url,
            headers=self.admin_headers(),
            query_string=query
        )
        self.assert200(response)
        self.assertEqual(response.json, expected)

    def test_group_users_get_list(self):
        group = mixer.blend(Group, company_id=self.company_id)
        uri = self.URI % group.id
        query = 'page=1&page_size=5'
        users = mixer.cycle(10).blend(
            User, groups=[group], company_id=self.company_id)
        user_schema = UserSchema()
        expected = {
            'meta': {
                'total_count': 10,
                'page_count': 2,
                'current_page': 1,
                'page_size': 5
            },
            'list': user_schema.dump(users[:5], many=True).data
        }

        response = self.client.get(
            uri,
            base_url=self.base_url,
            headers=self.admin_headers(),
            query_string=query
        )
        self.assert200(response)
        self.assertEqual(response.json, expected)

    def test_group_users_post(self):
        group = mixer.blend(Group, company_id=self.company_id)
        group_id = group.id
        uri = self.URI % group_id
        users = mixer.cycle(5).blend(User, company_id=self.company_id)
        user_ids = list(map(lambda item: item.id, users))

        response = self.client.post(
            uri,
            base_url=self.base_url,
            headers=self.admin_headers(),
            data=json.dumps({
                'user_ids': user_ids
            })
        )
        self.assert200(response)

        for user in users:
            self.assertIn(group, user.groups)

    def test_group_users_delete(self):
        group = mixer.blend(Group, company_id=self.company_id)
        group_id = group.id
        uri = self.URI % group_id
        users = mixer.cycle(5).blend(
            User, groups=[group], company_id=self.company_id)

        user_ids_list = list(map(lambda item: item.id, users))
        user_ids_to_keep = user_ids_list[3:]
        user_ids_to_delete = list(map(lambda item: item.id, users[:3]))

        response = self.client.delete(
            uri,
            base_url=self.base_url,
            headers=self.admin_headers(),
            data=json.dumps({
                'user_ids': user_ids_to_delete
            })
        )
        self.assert200(response)

        for user in group.users:
            self.assertIn(user.id, user_ids_to_keep)


if __name__ == '__main__':
    unittest.main()
