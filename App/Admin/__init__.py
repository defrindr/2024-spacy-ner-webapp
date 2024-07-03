from . import controller
from App.Admin.middleware import CheckIsLoggedAdmin
from App.Extensions.routes import Routes
from App.Admin.Uploader import Module as UploaderModule
from flask import Blueprint, render_template

Module = Blueprint('admin', __name__, template_folder="../Templates/Admin")

registerRoute = Routes(Module)

registerRoute.middleware(CheckIsLoggedAdmin)
registerRoute.get("/", controller.index)

Module.register_blueprint(UploaderModule, url_prefix="/uploader")

# @Module.errorhandler(Exception)
# def handle_exception(e):
#     # Return a user-friendly error message
#     if hasattr(e, "code"):
#         code = e.code
#     else:
#         code = 500
#     return render_template('error_generic.html', message=str(e), code=code), code
