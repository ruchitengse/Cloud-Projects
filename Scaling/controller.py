'''
Created on Apr 25, 2016

@author: Ruchi.U
'''
import mysql_database
import hashlib
from nosql_database import NoSQL_DB
from aws_s3 import AWS
import config
import os
from datetime import datetime
from mysql_database import MySQL_DB

def authorize_user(username, password):
    dbConnection = mysql_database.MySQL_DB()
    password = hash_password(password)
    valid_login = dbConnection.verify_login(username, password)
    return valid_login

def hash_password(password):
    m = hashlib.sha224(password)
    return m.hexdigest()

def fetch_images():
    nosql = NoSQL_DB()
    return nosql.get_all_items();

def create_user(username, password):
    password = hash_password(password)
    mysqldb = MySQL_DB()
    return mysqldb.create_user(username, password)

def insert_comments(username, image_id, posted_by, comment):
    nosqldatabase = NoSQL_DB()
    nosqldatabase.insert_comments(image_id, posted_by, username, comment)
    return "Comment Posted Successfully"

def upload_image(username, image):
    
    now = datetime.now();
    file_id = username + "_" + now.strftime('%Y%m%d%H%M%S')
    file_contents = image.read()
    file_name = username + "_" + image.filename
    file_path = os.path.join(file_name);
    with open(file_path, "wb") as f:
        f.write(file_contents);

    aws = AWS()
    aws.upload_file(file_path, file_id)
    link = config.BUCKET_LINK + config.BUCKET_NAME + "/" + file_id;
    image_json = {"username": username, "filename": file_name, "link": link, "id": file_id}
    nosql_db = NoSQL_DB()
    nosql_db.insert_image(image_json)
    
def delete_image(username, image_id):
    aws = AWS()
    aws.delete_image(image_id);
    nosqldb = NoSQL_DB()
    nosqldb.delete_image(image_id, username);