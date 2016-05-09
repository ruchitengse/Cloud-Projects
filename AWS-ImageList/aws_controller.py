'''
Created on Feb 3, 2016

@author: Ruchi.U
'''
from aws import AWS;
import config
import os
import hashing
import urllib2
class AWS_Controller:
    
    def upload_file(self, file_to_upload, bucket_name, quota):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket(bucket=bucket_name);
        return aws_conn.upload_file(file_to_upload, checkSize=True, size=quota);
    
    def view_files(self, bucket_name):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket(bucket=bucket_name);
        objects_list = aws_conn.view_files();
        files_list = dict()
        for image_object in objects_list:
            extension = image_object.key.split(".")[1].strip();
            link = config.BUCKET_LINK + bucket_name + "/" + image_object.key;
            if extension == "txt":
                link = self.read_text_file(link)
            files_list[image_object.key] = [image_object.key, link, image_object.last_modified, image_object.size]
        return files_list
        
    def delete_file(self, file_name, bucket_name):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket(bucket=bucket_name);
        aws_conn.delete_file(file_name);
    
    def download_file(self, file_name, bucket_name):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket(bucket=bucket_name);
        file_path =  aws_conn.download_files(file_name);
        with open(file_path, "rb") as f:
            data = f.read();
        file_name = os.path.basename(file_path);
        return file_name, data
    
    ## FOR PASSWORD ADD CODE HERE
    def authenticate(self, login_name, password = ''):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket('logindataaws');
        file_path = aws_conn.authenticate_user_name();
        f = open(file_path)
        for line in f:
            line = line.strip();
            username = line.split(",")[0].strip();
            print username;
            if (login_name == username):
                password_1 = line.split(",")[1].strip();
                if password == password_1:
                    space_quote = line.split(",")[2].strip();
                    return True, space_quote
        return False, 0
    
    def get_item_quota(self):
        aws_conn = AWS();
        aws_conn.aws_connect_to_bucket('logindataaws');
        space_quota = aws_conn.get_quota();
        f = open(space_quota)
        for line in f:
            line = line.strip();
            item_size = line.split(",")[0].strip();
            lifetime = line.split(",")[1].strip();
            return item_size, lifetime
    
    def read_text_file(self, link):
        data = urllib2.urlopen(link)
        i = 1;
        data_line = ""
        for line in data:
            data_line += line;
            i += 1;
            if(i > 5):
                break;
        return data_line;