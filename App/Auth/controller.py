import hashlib
import random
from flask import current_app, render_template, url_for, request, flash, redirect
from glob import glob

from App.Models.User import Role, User
from .auth_session import loggedInUser, setSessionAuth, destroySessionAuth


def _randomBackground():
    list_background = glob(
        "*", root_dir=current_app.root_path + "/Static/login")
    length_of_image = len(list_background)

    return list_background[random.randint(0, length_of_image - 1)]


def login():
    if loggedInUser() != None:
        return redirect(url_for('admin.index'))
    # bg_url = url_for("static", filename=f'login/{_randomBackground()}')
    return render_template("login.html")


def loginAction():
    username = request.form['username']
    password = str(request.form['passwd']).encode()
    hash_passwd = hashlib.md5(password).hexdigest()

    # Check if User Exist
    user = User.query.filter(User.username == username, User.flag == 1).first()
    if user is None:
        flash("Identitas tidak ditemukan")
        return redirect(url_for('auth.login'))

    # Check if Password matched
    if user.password != hash_passwd:
        flash("Identitas tidak ditemukan")
        return redirect(url_for('auth.login'))

    setSessionAuth(user.id, user.username, user.role)
    if user.role == Role.ADMIN:
        return redirect(url_for('admin.index'))
    else:
        return redirect(url_for('mahasiswa.index'))


def logoutAction():
    destroySessionAuth()
    return redirect(url_for('auth.login'))
