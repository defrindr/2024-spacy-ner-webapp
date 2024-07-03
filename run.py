from App import app, create_app
from App.Core.config import Config


conf = Config()
create_app(app, conf)

if __name__ == "__main__":
    app.run(port=Config.APP_PORT, debug=True)
