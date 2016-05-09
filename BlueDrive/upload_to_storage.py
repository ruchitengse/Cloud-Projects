#!/bin/env python
'''
Created on Jan 28, 2016

@author: Ruchi.U
'''
import os;
from flask import Flask;
from flask import render_template, request;
import fileupload
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('upload_to_storage.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file_to_upload = request.files['file_upload'];
    response = fileupload.FileUpload().upload_file_to_cloud(file_to_upload);
    return response;    
    
port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))