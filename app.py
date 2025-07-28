from config.config import config
from webapp import app

if __name__ == "__main__":
    app.run(host=config.FLASK_HOST,port=config.FLASK_PORT,debug=config.FLASK_DEBUG)