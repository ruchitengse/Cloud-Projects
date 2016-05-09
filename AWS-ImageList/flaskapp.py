'''
Created on Feb 3, 2016

@author: Ruchi.U
'''
from flask import Flask, session
from flask import request
import aws_controller
from flask.templating import render_template
from flask.helpers import make_response
import config
 
app = Flask(__name__, template_folder='templates', instance_relative_config=True)

@app.route("/logout")
def logout():
    return render_template('login_page.html')

@app.route("/login", methods=["POST"])
def view_images():
    user_name = request.form['user_name']
    password = request.form['password']
    aws_ctrl = aws_controller.AWS_Controller()
    is_valid, space_quota = aws_ctrl.authenticate(user_name, password)
    quota = int(space_quota)
    if is_valid:
        bucket_name = user_name + config.RANDOM_STRING;
        bucket_name =  bucket_name.lower();
        aws_ctrl = aws_controller.AWS_Controller()
        files_list = aws_ctrl.view_files(bucket_name=bucket_name)
        return render_template('image_list.html', response_value = None, files_list = files_list, bucket_name = bucket_name, quota = quota)
    else:
        return render_template('login_page.html', response_value = "Invalid User")

@app.route("/")
def login_page():
    return render_template('login_page.html')
    
@app.route("/upload", methods=["POST"])
def upload_images():
    file_to_upload = request.files["file_to_upload"]
    bucket_name = request.form["bucket_name"]
    quota = request.form["quota"]
    aws_ctrl = aws_controller.AWS_Controller();
    response = aws_ctrl.upload_file(file_to_upload, bucket_name, int(quota))
    files_list = aws_ctrl.view_files(bucket_name=bucket_name)
    return render_template('image_list.html', response_value = response, files_list = files_list, bucket_name = bucket_name, quota = quota)
 
@app.route("/delete", methods=["POST"])
def delete_images():
    file_to_delete = request.form["file_to_delete"]
    bucket_name = request.form["bucket_name"]
    quota = request.form["quota"]
    aws_ctrl = aws_controller.AWS_Controller()
    response = aws_ctrl.delete_file(file_to_delete, bucket_name)
    files_list = aws_ctrl.view_files(bucket_name)
    return render_template('image_list.html', response_value = response, files_list = files_list, bucket_name = bucket_name, quota=quota)
 
@app.route("/download", methods=["POST"])
def download_images():
    file_to_download = request.form["file_to_download"]
    bucket_name = request.form["bucket_name"]
    quota = request.form["quota"]
    aws_ctrl = aws_controller.AWS_Controller()
    file_name, data = aws_ctrl.download_file(file_to_download, bucket_name)
    response = make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename="+file_name;
    return response;

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5000)