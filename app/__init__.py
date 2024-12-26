import os

from flasgger import Swagger
from flask_migrate import Migrate

from .admin import admin
from .cli_commands import create_admin
from .config import Config
from .models import db
from .views import app

app.config.from_object(Config)
app.config["SWAGGER"] = {
    "title": "My Test Task",
    "uiversion": 3,
    "openapi": "3.0.0",
}


SWAGGER_YAML_PATH = os.path.join(os.path.dirname(__file__), "swagger.yaml")
swagger = Swagger(app, template_file=SWAGGER_YAML_PATH)
app.debug = True
app.jinja_env.cache = None

db.init_app(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)
