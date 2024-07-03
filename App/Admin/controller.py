from flask import render_template
from App.Auth.auth_session import loggedInUser


def index():
    return render_template('index.html')
