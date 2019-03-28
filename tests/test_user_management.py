import pytest
from unittest import mock
from messenger_server.user_management import OnlineUser, UserManager


@pytest.fixture(scope="module")
def online_user():
    return UserManager.sign_in("online_user", mock.Mock())


class TestUserManagement:
    def test_get_user_by_wrong_key(self, online_user):
        """Check if None is returned for non-existent key"""
        key = online_user.key

        assert UserManager.get_online_user_by_key(key + 1) is None

    def test_get_user_by_key(self, online_user):
        """Check if an OnlineUser object is returned for a proper key"""
        key = online_user.key

        assert isinstance(UserManager.get_online_user_by_key(key), OnlineUser)

    def test_get_user_by_wrong_login(self, online_user):
        """Check if None is returned for non-existent login"""
        login = online_user.login

        assert UserManager.get_online_user_by_login(login + "_fake") is None

    def test_get_user_by_login(self, online_user):
        """Check if an OnlineUser object is returned for a proper login"""
        login = online_user.login

        assert isinstance(UserManager.get_online_user_by_login(login), OnlineUser)
