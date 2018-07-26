from flask import render_template, redirect, url_for, flash
from forms.upload_form import CheckFile
import os
import config
import encryption
import database

app = None
upload_dir = None  # 文件上传/下载路径
filelist = None

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS  # 允许上传的文件格式
ALLOWED_FILE_SIZE = config.ALLOWED_FILE_SIZE  # 允许上传的文件大小MB


def init(_app):
    global app
    global upload_dir
    app = _app
    upload_dir = os.path.join(
        app.instance_path, 'upload'
    )  # 将文件上传到项目的upload文件夹下
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        # upload_dir = r'D:\Users\蛮小白\Desktop\test\upload'


def allowed_file(filename):  # 检查文件格式是否合法
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_size(size):  # 检查文件大小是否合法
    return size <= ALLOWED_FILE_SIZE


def upload_file():
    form = CheckFile()
    # database.add_filehash("test","lycheng")
    if form.validate_on_submit():
        f = form.image.data
        size = len(f.read())
        if allowed_file(f.filename):
            if allowed_size(size):
                f.seek(0)
                f.save(os.path.join(upload_dir, f.filename))
                flash('Upload success。')
                return redirect(url_for('upload'))
            else:
                flash('上传失败，文件大小：<=10M')
        else:
            flash('上传失败，允许上传的文件类型：office文档、常见图片类型')
    return render_template('./upload/upload.html', form=form)

def file_list():  # 返回已经上传的文件列表
    name=''
    for parent, dirname, filenames in os.walk(upload_dir):
        filelist = filenames
    return render_template('./upload/download.html', message=filelist)

def download(filename):
    return send_from_directory(upload_dir, filename, mimetype='application/octet-stream')