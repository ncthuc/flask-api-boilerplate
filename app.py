import os

from src import create_app

app = create_app(os.getenv('DEPLOYMENT_ENV') or 'dev')

if __name__ == '__main__':
    app.run()
