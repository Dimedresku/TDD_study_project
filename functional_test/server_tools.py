from fabric.api import run
from fabric.context_managers import settings


def _get_manage_dot_py(host):
    return f'~/sites/{host}/virtualenv/bin/python3.8 ~/sites/{host}/source/manage.py'


def reset_database(host):
    manage_dot_py = _get_manage_dot_py('superlists-staging')
    with settings(host_string='dmitriy@localhost', port=8022, password='1'):
        run(f'{manage_dot_py} flush --noinput')


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py('superlists-staging')
    with settings(host_string='dmitriy@localhost', port=8022, password='1'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key