from flask import render_template, request, flash, redirect, url_for, send_from_directory
from App.Auth.auth_session import loggedInUser
from App.Core.database import db
import App.Models.Crawler as CrawlerInstance
from App.Models.Crawler import Crawler
from App.Auth.auth_session import SESS_AUTH_ID, getSessionAuth
from sqlalchemy import or_
from flask import current_app as app
from App.Utils.Validator import Validator
import os
from werkzeug.utils import secure_filename
import time
from App.Core.spacy import spacy_ner
import json
from .crawler_helper import CrawlerHelper
import subprocess

module = "admin.crawler"
viewLayout = 'Admin/Crawler/'


crawlerHelper = CrawlerHelper()


def index():
    title = "Crawler Data Tweets"

    headers = ['No', 'Dokumen', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    session = getSessionAuth()
    userId = session[SESS_AUTH_ID]

    baseQuery = CrawlerInstance.ActiveQuery()
    if userId != 1:
        baseQuery = baseQuery.where(Berita.user_id == userId)

    if search != '':
        # baseQuery = baseQuery.filter(
        #     CrawlerInstance.Crawler.nama.like(f"%{search}%")
        # )
        pass

    total_data = baseQuery.count()
    pagination = baseQuery.paginate(page=page, per_page=per_page)
    start_data = page * per_page - per_page
    len_items = len(pagination.items)

    return render_template(
        viewLayout + 'index.html',
        title=title,
        module=module,
        pagination=pagination,
        len_items=len_items,
        headers=headers,
        start_data=start_data,
        per_page=per_page,
        total_data=total_data,
        search=search
    )


def create():
    title = "Tambah Data"
    return render_template(
        viewLayout + 'create.html',
        title=title,
        module=module
    )


def store():
    redirected_error = url_for(f'{module}.create')
    path = app.config['BASE_PATH'] + '/App/Static/uploads'
    source_path = path + '/source/'
    result_path = path + '/result/'

    required_fields = ["token", "keyword", "limit"]
    form = request.form.to_dict()

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    source_filename = secure_filename(str(int(time.time()))+"_scrapper.csv")
    result = result_path + source_filename
    crawlerHelper.run(
        source_filename,
        form['keyword'],
        form['limit'],
        form['token'],
    )

    subprocess.call(
        ["mv", os.getcwd()+'/tweets-data/'+source_filename, result]
    )

    form['result'] = result.replace(os.getcwd()+'/App/Static', '')

    # save model
    model = CrawlerInstance.assign(form=form)

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))
    pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def destroy(id):
    Crawler.query.filter(Crawler.id == id).delete()
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index'))
    pass
