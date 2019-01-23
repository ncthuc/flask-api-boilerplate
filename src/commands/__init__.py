from src.commands.user_command import user_cli


def init_command(app, **kwargs):
    """
    :param flask.Flask app: the app
    :param kwargs:
    :return:
    """

    app.cli.add_command(user_cli)
