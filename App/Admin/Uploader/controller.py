from flask import render_template, request, flash, redirect, url_for, send_from_directory
from App.Auth.auth_session import loggedInUser
from App.Core.database import db
import App.Models.Uploader as UploaderInstance
from App.Models.Uploader import Uploader
from App.Auth.auth_session import SESS_AUTH_ID, getSessionAuth
from sqlalchemy import or_
from flask import current_app as app
from App.Utils.Validator import Validator
import os
from werkzeug.utils import secure_filename
import time
from App.Core.spacy import spacy_ner
import json

module = "admin.uploader"
viewLayout = 'Admin/Uploader/'

ALLOWED_EXTENSIONS = {'csv'}


def index():
    title = "Klasifikasi Spacy NER"

    headers = ['No', 'Dokumen', 'Aksi']

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '', type=str)

    session = getSessionAuth()
    userId = session[SESS_AUTH_ID]

    baseQuery = UploaderInstance.ActiveQuery()
    if userId != 1:
        baseQuery = baseQuery.where(Berita.user_id == userId)

    if search != '':
        baseQuery = baseQuery.filter(
            UploaderInstance.Uploader.nama.like(f"%{search}%")
        )
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


def unduhtemplate():
    path = app.config['BASE_PATH'] + '/App/Static/uploads'
    return send_from_directory(path, 'template.csv')
    pass


def show(id):
    title = "Grafik Wilayah Kriminalitas"
    data = Uploader.query.filter(Uploader.id == id).first()
    dict_result = json.loads(data.result)
    keys = list(dict_result.keys())
    values = list(dict_result.values())
    return render_template(
        viewLayout + 'show.html',
        title=title,
        module=module,
        data=data,
        keys=keys,
        values=values
    )


def create():
    title = "Tambah Kategori Baru"
    return render_template(
        viewLayout + 'create.html',
        title=title,
        module=module
    )


def store():
    print(11111)
    redirected_error = url_for(f'{module}.create')
    path = app.config['BASE_PATH'] + '/App/Static/uploads'
    source_path = path + '/source/'
    result_path = path + '/result/'
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(redirected_error)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(redirected_error)
        if file and allowed_file(file.filename):
            source_filename = secure_filename(
                str(int(time.time()))+"_"+file.filename)
            file.save(os.path.join(source_path, source_filename))
        else:
            flash('File not valid')
            return redirect(redirected_error)
    else:
        flash('Method Not Valid')
        return redirect(redirected_error)

    # print(source_filename)
    source_file = source_path+source_filename
    result_file = f"{result_path}{str(int(time.time()))}_result.json"
    predict = spacy_ner.predict(source_file, result_file)

    required_fields = ["nama", "file", "spacy", "result"]
    form = request.form.to_dict()
    form['file'] = source_file.replace(os.getcwd()+'/App/Static', '')
    form['spacy'] = result_file.replace(os.getcwd()+'/App/Static', '')
    form['result'] = json.dumps(predict)

    app_validator = Validator()
    app_validator.required(form, required_fields)
    if len(app_validator.errors) > 0:
        return app_validator.flashMessage().redirect(f'{module}.create')

    # save model
    model = UploaderInstance.assign(form=form)

    # commit
    db.session.add(model)
    db.session.commit()

    flash('Data telah ditambahkan', 'info')
    return redirect(url_for(f'{module}.index'))

    return
    pass


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def destroy(id):
    Uploader.query.filter(Uploader.id == id).delete()
    db.session.commit()
    flash('Data berhasil dihapus', 'info')
    return redirect(url_for(f'{module}.index'))
    pass
