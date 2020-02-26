import os
import dotenv

from src import create_app

dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), './.env'))
app = create_app()

if __name__ == '__main__':
    app.run()
