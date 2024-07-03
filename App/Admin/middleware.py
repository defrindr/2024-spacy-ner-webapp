from App.Auth.auth_session import SESS_AUTH_ROLE, getSessionAuth
from App.Models.User import Role
from flask import abort, redirect, url_for


def CheckIsLoggedAdmin():
    session = getSessionAuth()
    if (session[SESS_AUTH_ROLE] != Role.ADMIN):
        return abort(403)
        # return redirect(url_for('auth.login'))
