from flask import render_template, redirect, url_for, flash
from forms.upload_form import CheckFile
import os
import config
import encryption
from forms.dowmload_form import DownloadForm
from flask import send_from_directory
from io import BytesIO
import zipfile
app = None
upload_dir = None  # 文件上传/下载路径
download_dir=None   #下载路径
sign_dir=None   #签名路径
filelist = None

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS  # 允许上传的文件格式
ALLOWED_FILE_SIZE = config.ALLOWED_FILE_SIZE  # 允许上传的文件大小MB


def init(_app):
    global app
    global upload_dir,download_dir,sign_dir
    app = _app
    upload_dir = os.path.join(
        app.instance_path, 'upload'
    )  # 将文件上传到项目的upload文件夹下
    download_dir=os.path.join(
        app.instance_path,'download'
    )
    sign_dir=os.path.join(
        app.instance_path,'sign'
    )

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(sign_dir):
        os.makedirs(sign_dir)



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
        file_path = os.path.join(upload_dir, f.filename)
        sign_path=os.path.join(sign_dir,f.filename.split('.')[-2])
        if f.filename in file_list():
            flash('file exists')
            return redirect(url_for('upload_file'))
        data=f.read()
        size = len(data)
        if allowed_file(f.filename):
            if allowed_size(size):
                data_encryption = encryption.encryption_file(data)
                with open(file_path, 'wb') as file:
                    file.write(data_encryption)
                with open(sign_path,'wb') as file:
                    file.write(encryption.sign_file(data_encryption))
                flash('Upload success。')
                return redirect(url_for('upload_file'))
            else:
                flash('上传失败，文件大小：<=10M')
        else:
            flash('上传失败，允许上传的文件类型：office文档、常见图片类型')
    return render_template('./upload/upload.html', form=form)

def file_list():  # 返回已经上传的文件列表
    for parent, dirname, filenames in os.walk(upload_dir):
        filelist = filenames
    return str(filelist)

def download(filename):
    path=os.path.join(upload_dir,filename)
    sign_path=os.path.join(sign_dir,filename.split('.')[-2])
    with open(sign_path,'rb') as file:  #获取签名
        signdata=file.read()
    with open(path,'rb') as file:   #获取加密后数据
        filedata=file.read()
    sign=encryption.verify_file(signdata,filedata)
    if sign:
        d=encryption.decryption_file(path)
        with open(os.path.join(download_dir,filename),'wb') as file:
            file.write(d+b'\x00\x00\x00\x00')
        flash('success')
        return send_from_directory(download_dir, filename,mimetype='application/octet-stream')
    flash('verification failed')
    return redirect(url_for('filedownload'))


def download_anonmity(filename):
    dl_name = '{}.zip'.format(filename.split('.')[-2])
    with zipfile.ZipFile(os.path.join(download_dir,dl_name), 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(os.path.join(upload_dir, filename),filename)
        f.write(os.path.join(sign_dir,filename.split('.')[-2]),filename.split('.')[-2])
    return send_from_directory(download_dir, dl_name, mimetype='application/octet-stream')