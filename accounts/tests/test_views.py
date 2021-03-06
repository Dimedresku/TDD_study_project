from django.test import TestCase
from unittest.mock import patch, call

import accounts.views
from accounts.models import Token


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_home_page(self):
        '''test: redirects to home page'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'})
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sand_mail_to_address_from_post(self, mock_send_mail):
        '''test: send meessage to address from post'''
        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'noreplay@superlists')
        self.assertEqual(to_list, ['edith@example.com'])

    def test_adds_success_message(self):
        '''test: adds success message'''
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        }, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            'Check your email, you`ll find a message with a link '
            'that will log you into the site.'
        )
        self.assertEqual(message.tags, 'success')

    def test_create_token_associated_with_email(self):
        '''test: create token'''
        self.client.post('/accounts/send_login_email', data={'email': 'edith@example.com'})
        token = Token.objects.first()
        self.assertEqual(token.email, 'edith@example.com')

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        '''test: send link to login using token uid'''
        self.client.post('/accounts/send_login_email', data={'email': 'edith@example.com'})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwards = mock_send_mail.call_args
        self.assertIn(expected_url, body)


@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    '''test view for login in system'''

    def test_redirects_to_home_page(self, mock_auth):
        '''test: redirects to home page'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')

    def test_call_authenticate_with_uid_from_get_request(self, mock_auth):
        '''test: call authenticate with uid'''
        self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid='abcd123')
        )

    def test_calls_auth_login_with_user_if_there_is_one(self, mock_auth):
        '''test: call login if user existing'''
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_user_is_not_authenticated(self, mock_auth):
        '''test: does not login if user is not authenticated'''
        mock_auth.authenticate.return_value = None
        self.client.get('/accounts/login?token=abcd123')
        self.assertFalse(mock_auth.login.called)