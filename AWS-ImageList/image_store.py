'''
Created on Feb 3, 2016

@author: Ruchi.U
'''
from flask import Flask;
from flask import request;
import aws_controller
from flask.templating import render_template
import os;

app = Flask(__name__);

@app.route("/")
def view_images():
    aws_ctrl = aws_controller.AWS_Controller();
    files_list = aws_ctrl.view_files();
    return render_template('image_list.html', files_list = files_list, response_value = None)
    
@app.route("/upload", methods=["POST"])
def upload_images():
    file_to_upload = request.files["file_to_upload"];
    aws_ctrl = aws_controller.AWS_Controller();
    response = aws_ctrl.upload_file(file_to_upload);
    files_list = aws_ctrl.view_files();
    return render_template('image_list.html', response_value = response, files_list = files_list)

@app.route("/delete", methods=["POST"])
def delete_images():
    file_to_delete = request.form["file_to_delete"];
    aws_ctrl = aws_controller.AWS_Controller();
    response = aws_ctrl.delete_file(file_to_delete);
    files_list = aws_ctrl.view_files();
    return render_template('image_list.html', response_value = response, files_list = files_list)

@app.route("/download", methods=["POST"])
def download_images():
    file_to_download = request.form["file_to_download"];
    aws_ctrl = aws_controller.AWS_Controller();
    response = aws_ctrl.download_file(file_to_download);
    files_list = aws_ctrl.view_files();
    return render_template('image_list.html', response_value = response, files_list = files_list)

port = os.getenv('VCAP_APP_PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port), debug=True)