import click
from flask.cli import AppGroup
import logging

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
user_cli = AppGroup('user', help="Manage users in cli", context_settings=CONTEXT_SETTINGS)


@user_cli.command('create', help='Create a new user')
@click.argument('name')
def create_user(name):
    _logger.info(f"creating a new user `{name}`")


@user_cli.command('set_password', help='Set user password')
@click.argument('name', metavar='{user_name}')
@click.argument('password', metavar='{password}')
@click.option('--email', default=0, help='Send email notification')
def set_password(email, name, password):
    _logger.info(f"Setting new password for user `{name}` to `{password}`, "
                 f"email notification = {email}")

