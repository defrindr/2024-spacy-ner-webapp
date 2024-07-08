from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('crawler', __name__, template_folder="/Crawler")
registerRoute = Routes(Module)

registerRoute.get("/", controller.index)
registerRoute.get("/create", controller.create)
registerRoute.post("/store", controller.store)
# registerRoute.get("/show/<id>", controller.show)
# registerRoute.post("/update/<id>", controller.update)
registerRoute.post("/destroy/<id>", controller.destroy)
