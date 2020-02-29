# coding=utf-8
import logging

from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from src.api_admin import init_admin_api

__author__ = 'ThucNC'
_logger = logging.getLogger(__name__)


def create_app():
    import config
    import logging.config
    from src.api import init_api
    from src.model import init_model
    from src.commands import init_command

    app = Flask(__name__)
    app.config.from_object(config.Config)
    logging.config.fileConfig(app.config['LOGGING_CONFIG_FILE'], disable_existing_loggers=False)
    _logger.info(f"Starting application, db: {config.Config.SQLALCHEMY_DATABASE_URI}")

    init_api(app)
    init_admin_api(app)
    init_model(app)
    init_command(app)

    # app.config['DEBUG_TB_PROFILER_ENABLED'] = True
    # toolbar = DebugToolbarExtension(app)
    # toolbar.init_app(app)
    return app
