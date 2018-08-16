import os
import sys
from flask import Flask, request, redirect, url_for, flash, render_template, redirect
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
from flask import send_from_directory
sys.path.append('./src')
from database import dataBase
import numpy as np
import time


UPLOAD_FOLDER = './static/submitted_files'
ALLOWED_EXTENSIONS = set(['txt', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './submitted_files'

def get_users(fname):
    with open(fname, 'r') as fp:
        users = fp.readlines()
    return [item.rstrip("\n") for item in users]

def compute_score(targets, prediction_file):    
    try:
        predictions = np.genfromtxt(prediction_file)
        assert predictions.size==targets.size,('Number of labels are more than required' if predictions.size>targets.size else 'Number of labels are less than required')
        return 'OK', np.sum(predictions==targets)/targets.size
    except Exception as e:
        return e, 0.0

def check_user_validity(user):
    return user in g_users

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['UPLOAD_FOLDER']
})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    terminal_output = ''
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            user_id = filename.split(".")[0].lower()
            if check_user_validity(user_id):
                user_dir = user_id
                if not os.path.exists(os.path.join('static', 'submissions', user_dir)):
                    os.mkdir(os.path.join('static', 'submissions', user_dir), 755)
                timestamp = str(time.time())
                file.save(os.path.join('static', 'submissions', user_dir , user_id+"_"+timestamp))
                status, user_score = compute_score(targets, os.path.join('static', 'submissions', user_dir, user_id+"_"+timestamp))
                print(user_id+"_"+timestamp,user_score)
                if status == 'OK':
                    print("Got file from user", user_id, user_score)
                    user_details = db.update_score(user_id, user_score)
                    terminal_output+="<b>Rank:</b> %02d <br><b>Best score:</b> %0.5f <br><b>Current score:</b> %0.5f"%(user_details[1]+1,user_details[0],user_score)
                else:
                    terminal_output += "<b>Error: {}</b>".format(status)
            else:
                terminal_output += "<b>Invalid user!</b>"
        else:
            terminal_output += "<b>Check file extension. Allowed extension are txt/csv</b>"

    return '''
    <!doctype html>
    <title>COL 341 (A2)</title>
    <div align="center">
    <h1>Upload prediction file</h1>
    <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
        <input type=submit value=Upload>
        </p>
    </form>
    <p>
    %s
    <p>
    </div>
    '''%(terminal_output)
if __name__ == '__main__':
    db = dataBase()
    targets = None
    #print(os.getcwd())
    app.secret_key = 'super secret key'
    g_users = set(get_users(os.path.join('./data', 'usernames')))
    targets = np.genfromtxt(os.path.join('./data', 'target_imdb'))
    #app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host= '0.0.0.0')
