from flask import Flask
from flask.templating import render_template
from flask import request
import controller

application = app = Flask(__name__)

@app.route('/')
def start_page():
    '''Code for Login Page goes here'''
    return render_template('login_page.html')

@app.route("/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    login_successful = controller.authorize_user(username, password);
    if login_successful:
        image_info = controller.fetch_images()
        return render_template('home_page.html', username = username, image_info = image_info)
    else:
        return render_template('login_page.html', msg = "Incorrect username and/or password!!")
 
@app.route("/upload_image",methods=["POST"])
def upload_image():
    print "Upload Image"
    file_name = request.files['file_name']
    username = request.form['username']
    controller.upload_image(username, file_name)
    image_info = controller.fetch_images();
    return render_template('home_page.html', username = username, image_info = image_info)
 
@app.route("/post_comments", methods=["POST"])
def post_comments():
    '''
    Get username
    Get comment
    Get id
    Retrieve json for id
    Form json with comment.
    Update json in db
    '''
    username = request.form['username']
    image_id = request.form['image_id']
    posted_by = request.form['posted_by']
    comment = request.form['comment']
    msg = controller.insert_comments(username, image_id, posted_by, comment)
    image_info = controller.fetch_images();
    return render_template('home_page.html', username = username, image_info = image_info, msg = msg)
     
@app.route("/delete_image", methods=["GET"])
def delete_image():
    image_id = request.args['image_id']
    username = request.args['username']
    controller.delete_image(username, image_id)
    image_info = controller.fetch_images()
    return render_template('home_page.html', username = username, image_info = image_info)

@app.route("/logout", methods=["GET"])
def logout():
    return render_template('login_page.html')

@application.route('/register', methods=["GET"])
def register():
    return render_template('register.html')

@app.route('/create_user', methods=["POST"])
def create_user():
    username = request.form['username']
    password = request.form['password']
    response = controller.create_user(username, password)
    if response:
        return render_template('register.html', msg = "Could not register user")
    else:
        return render_template('login_page.html')
 
if __name__ == '__main__':
    app.run()