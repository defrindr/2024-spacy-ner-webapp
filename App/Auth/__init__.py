from App.Extensions.routes import Routes
from flask import Blueprint
from . import controller

Module = Blueprint('auth', __name__, template_folder="../Templates/Auth")

registerRoute = Routes(Module)

registerRoute.get("/", controller.login)
registerRoute.post("/login", controller.loginAction)
registerRoute.post("/logout", controller.logoutAction)
