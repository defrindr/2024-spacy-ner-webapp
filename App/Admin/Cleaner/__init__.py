from . import controller
from App.Extensions.routes import Routes
from flask import Blueprint

Module = Blueprint('cleaner', __name__, template_folder="/Cleaner")
registerRoute = Routes(Module)

registerRoute.get("/", controller.index)
registerRoute.get("/unduhtemplate", controller.unduhtemplate)
registerRoute.get("/create", controller.create)
registerRoute.post("/store", controller.store)
# registerRoute.get("/show/<id>", controller.show)
# registerRoute.post("/update/<id>", controller.update)
registerRoute.post("/destroy/<id>", controller.destroy)
