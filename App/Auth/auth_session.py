from flask import session

from App.Models.User import Role, User

SESS_AUTH_ID = "id"
SESS_AUTH_USERNAME = "username"
SESS_AUTH_ROLE = "role"


def getSessionAuth():
    return {
        SESS_AUTH_ID: session.get(SESS_AUTH_ID),
        SESS_AUTH_USERNAME: session.get(SESS_AUTH_USERNAME),
        SESS_AUTH_ROLE: session.get(SESS_AUTH_ROLE),
    }


def setSessionAuth(id, username, role=Role):
    session[SESS_AUTH_ID] = id
    session[SESS_AUTH_USERNAME] = username
    session[SESS_AUTH_ROLE] = role


def destroySessionAuth():
    session.pop(SESS_AUTH_ID)
    session.pop(SESS_AUTH_USERNAME)
    session.pop(SESS_AUTH_ROLE)


def loggedInUser():
    id = session[SESS_AUTH_ID]
    return User.query.filter(
        User.flag == 1,
        User.id == id
    ).first()
