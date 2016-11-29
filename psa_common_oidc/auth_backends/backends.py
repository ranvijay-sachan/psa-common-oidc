"""
This file contains Django authentication backends. For more information visit
https://docs.djangoproject.com/en/dev/topics/auth/customizing/.
@author : ranvijay sachan
"""
from django.conf import settings
from social.backends.oauth import BaseOAuth2
from social.backends.open_id import OpenIdConnectAuth


class CommonOAuth2Mixin(object):
    ACCESS_TOKEN_METHOD = 'POST'
    REDIRECT_STATE = False
    ID_KEY = 'email'
    USER_INFO_URL = None

    def get_user_permissions(self, access_token):
        # TODO: Do we need to worry about refreshing the token?
        data = self.get_json(
            self.USER_INFO_URL,
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        )
        return data['permissions']


class AnyOAuth2(CommonOAuth2Mixin, BaseOAuth2):
    name = 'any-oauth2'
    AUTHORIZATION_URL = ''
    ACCESS_TOKEN_URL = ''
    USER_INFO_URL = ''

    # optional
    REVOKE_TOKEN_URL = ''
    REVOKE_TOKEN_METHOD = 'GET'
    DEPRECATED_DEFAULT_SCOPE = [
        '',
    ]

    EXTRA_DATA = [
        ('email', 'id'),
        ('code', 'code'),
        ('expires_in', 'expires'),
        ('refresh_token', 'refresh_token', True),
    ]

    def get_user_details(self, response):
        """Return user details from edX account"""
        return {
            'username': response.get('username'),
            'email': '',
            'fullname': '',
            'first_name': '',
            'last_name': ''
        }


class AnyOpenIdConnect(CommonOAuth2Mixin, OpenIdConnectAuth):
    name = 'any-oidc'
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
    ID_TOKEN_ISSUER = settings.ANY_ID_TOKEN_ISSUER
    AUTHORIZATION_URL = settings.ANY_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.ANY_ACCESS_TOKEN_URL
    USER_INFO_URL = settings.ANY_USER_INFO_URL

    def user_data(self, _access_token, *_args, **_kwargs):
        return self.id_token

    def get_user_details(self, response):
        return {
            # u'username': response['username'],
            u'email': response['email'],
            u'full_name': response['name'],
            u'first_name': response['given_name'],
            u'last_name': response['family_name']
        }
