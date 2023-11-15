from app import create_app
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
