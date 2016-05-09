#!/bin/env python
'''
Created on Jan 28, 2016

@author: Ruchi.U
'''
import os;
from flask import Flask;
from flask import render_template, request;
from cloudantdb import CloudantDB
from flask.helpers import make_response
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('mainpage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file_to_upload = request.files['file_upload'];
    response = CloudantDB().upload_file(file_to_upload);
    return response;    
    
@app.route('/download', methods=['POST'])
def download_file():
    file_name = request.form['file_name'];
    version = int(request.form["version"])
    file_name, data = CloudantDB().download_file_from_db(file_name, version);
    response = make_response(data);
    response.headers["Content-Disposition"] = "attachment; filename="+file_name;
    return response;

@app.route('/list')
def list_all_in_db():
    cd = CloudantDB()
    cd.connect_to_db();
    return str(cd.list_all_in_db());

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)