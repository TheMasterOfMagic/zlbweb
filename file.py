from flask import render_template, redirect, url_for, flash
from forms.upload_form import CheckFile
import os
import config
import encryption
from forms.dowmload_form import DownloadForm
from flask import send_from_directory
from io import BytesIO
import zipfile
import hashlib
app = None
upload_dir = None  # 文件上传/下载路径
download_dir=None   #下载路径
sign_dir=None   #签名路径
hash_dir=None
filelist = []

ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS  # 允许上传的文件格式
ALLOWED_FILE_SIZE = config.ALLOWED_FILE_SIZE  # 允许上传的文件大小MB


def init(_app):
    global app
    global upload_dir,download_dir,sign_dir,hash_dir
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
    hash_dir = os.path.join(
        app.instance_path, 'hash'
    )

    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(sign_dir):
        os.makedirs(sign_dir)
    if not os.path.exists(hash_dir):
        os.makedirs(hash_dir)

def allowed_file(filename):  # 检查文件格式是否合法
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def allowed_size(size):  # 检查文件大小是否合法
    return size <= ALLOWED_FILE_SIZE

def getMd5(filedata,filename):
    '''将字典的键设为每个文件的md5，值为不同用户上传的文件名'''
    myhash=hashlib.md5()
    myhash.update(filedata)
    with open(os.path.join(hash_dir,'hash'),'r')as file:
        my_dict = file.read()
    my_dict=dict(my_dict) if my_dict=='' else eval(my_dict)
    if my_dict.get(myhash.hexdigest())==None:
        return False
    if filename not in my_dict[myhash.hexdigest()]:
        my_dict[myhash.hexdigest()].append(filename)
    with open(os.path.join(hash_dir,'hash'),'w')as file:
        file.write(str(my_dict))
    return True

def saveMd5(filedata,filename):
    '''第一次被上传的文件建立键值对，{md5:filename}'''
    myhash=hashlib.md5()
    myhash.update(filedata)
    with open(os.path.join(hash_dir,'hash'),'r')as file:
        my_dict=file.read()
    my_dict=dict(my_dict) if my_dict=='' else eval(my_dict)
    my_dict[myhash.hexdigest()]=[filename]
    with open(os.path.join(hash_dir,'hash'),'w')as file:
        file.write(str(my_dict))

def file_list():  # 返回已经上传的文件列表
    global filelist
    with open(os.path.join(hash_dir,'hash'),'r')as file:
        my_dict = file.read()
    my_dict=dict(my_dict) if my_dict=='' else eval(my_dict)
    for i in my_dict:
        filelist.extend(list(my_dict[i]))
    return str(filelist)

def get_name(filename):
    '''不同用户上传/下载相同文件时用的文件名不同，但服务器只保存一次该文件，
    此处通过用户输入的文件名获取服务器保存的该文件的真实文件名'''
    with open(os.path.join(hash_dir,'hash'),'r')as file:
        my_dict = file.read()
    my_dict=dict(my_dict) if my_dict=='' else eval(my_dict)
    for i in my_dict:
        if filename in my_dict[i]:
            return my_dict[i][0]
    return False

def upload_file():

    '''上传文件，限制文件大小，格式并对文件加密保存'''
    form = CheckFile()
    # database.add_filehash("test","lycheng")
    if form.validate_on_submit():
        f = form.image.data
        file_path = os.path.join(upload_dir, f.filename)
        sign_path=os.path.join(sign_dir,f.filename.split('.')[-2])
        data=f.read()
        size = len(data)
        if allowed_file(f.filename):
            if allowed_size(size):
                if getMd5(data, f.filename):  # 如果返回True，表示该文件已经上传过，可以秒传
                    flash('Upload success。')
                    return redirect(url_for('upload_file'))
                if f.filename in file_list():  # 如果为真，表示服务器已存在同名(不同内容)文件，需改名
                    flash('服务器存在同名文件，请重试')
                    return redirect(url_for('upload_file'))
                saveMd5(data,f.filename)#保存文件的md5
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

def download(name):
    '''下载服务器端保存的文件'''
    if get_name(name):
        filename=get_name(name)
    else:
        print('file name error')
        flash('file name error')
        return redirect(url_for('filedownload'))
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
        return send_from_directory(download_dir, filename, as_attachment=True)
    flash('verification failed')
    return redirect(url_for('filedownload'))


def download_anonmity(name):
    if get_name(name):
        filename=get_name(name)
    else:
        print('file name error')
        flash('file name error')
        return redirect(url_for('filedownload'))
    dl_name = '{}.zip'.format(filename.split('.')[-2])
    with zipfile.ZipFile(os.path.join(download_dir,dl_name), 'w', zipfile.ZIP_DEFLATED) as f:
        f.write(os.path.join(upload_dir, filename),filename)
        f.write(os.path.join(sign_dir,filename.split('.')[-2]),filename.split('.')[-2])

    return send_from_directory(download_dir, dl_name, mimetype='application/octet-stream')