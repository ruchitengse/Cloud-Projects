
'''
Created on Feb 3, 2016

@author: Ruchi.U
'''
import boto3
import os
import MySQLdb
import botocore
from datetime import datetime
from datetime import timedelta
import hashing
class AWS:
    
    def aws_connect_to_bucket(self, bucket='cloud-image-store'):
        self.aws_resource = boto3.resource('s3')
        self.bucket = self.aws_resource.Bucket(bucket)
        exists = True;
        try:
            self.aws_resource.meta.client.head_bucket(Bucket=bucket)
        except botocore.exceptions.ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404 or error_code == 403:
                exists = False
            
    def upload_file(self, file_to_upload, secure=False, checkSize=False, size=9):
        
        item_size, lifetime = self.get_quota();
        
        UPLOAD_FOLDER = "/var/www/html/flaskapp/testdir"
        file_name = file_to_upload.filename;
        file_contents = file_to_upload.read();
        if checkSize:
            object_size = len(file_contents)/1024;
            if object_size > item_size:
                return "Item size is more than specified"
            all_objects = self.view_files();
            totalSize = 0;
            for object in all_objects:
                totalSize += (object.size/(1024));
            totalSize += (len(file_contents)/(1024));
            if totalSize > size:
                return "Bucket size limit exceeded"
        
        file_path = os.path.join(UPLOAD_FOLDER, file_name);
        with open(file_path, "wb") as f:
            f.write(file_contents);
        if secure:
            file_path = hashing.encrypt_file(file_path);
            print file_path;
        self.bucket.upload_file(file_path, file_name, ExtraArgs={'ACL':'public-read'});
        object = self.aws_resource.Object('mikecloud-project-image-list', 'SpaceQuota.txt')
        object.expires(datetime.now() + timedelta(0,30))
        object.load()
        return "File uploaded successfully";

    def view_files(self):
        return self.bucket.objects.all()
            
    def download_files(self, file_name, secure=False):
        DOWNLOAD_FOLDER = "/var/www/html/flaskapp/downloads"
        file_path = os.path.join(DOWNLOAD_FOLDER, file_name);
        self.bucket.download_file(Key=file_name, Filename=file_path)
        if secure:
            downloaded_file_path = hashing.decrypt_file(file_path, file_name)
            return downloaded_file_path;
        else:
            return file_path;
    
    def delete_file(self, file_name):
        DeleteObj = {
            'Objects': [{
                'Key': file_name            
            }]
        }
        self.bucket.delete_objects(Delete=DeleteObj);
        
    def authenticate_user_name(self):
        DOWNLOAD_FOLDER = "/var/www/html/flaskapp/downloads"
        file_path = os.path.join(DOWNLOAD_FOLDER, 'UserAccessList.txt')
        self.bucket.download_file(Key='UserAccessList.txt', Filename=file_path)
        return file_path
    
    def get_quota(self):
        DOWNLOAD_FOLDER = "/var/www/html/flaskapp/downloads"
        file_path = os.path.join(DOWNLOAD_FOLDER, 'SpaceQuota.txt')
        self.bucket.download_file(Key='SpaceQuota.txt', Filename=file_path)
        f = open(file_path)
        for line in f:
            line = line.strip();
            item_size = line.split(",")[0].strip();
            lifetime = line.split(",")[1].strip();
    
    def authenticate_user_name_password_db(self, login_name, password):
        connection = MySQLdb.connect(host="clouddatabase.cmac8hwmegyk.us-west-2.rds.amazonaws.com",user="ruchitengse",passwd="cloudpassword",db="login_name",port=3306)
        cursor = connection.cursor()
        sql = "SELECT * FROM login_details where username = '%s' and password = '%s'" %(login_name, password)
        cursor.execute(sql);
        results = cursor.fetchall();
        if not results:
            return False;
        return True;
    
    def put_life_cycle_configuration(self, bucket):
        kwargs = {'aws_access_key_id':'AKIAIRAB5ZYWDZMT3PXQ', 'aws_secret_access_key':'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', 'region_name':'us-west-2'}
        client = boto3.client('s3', **kwargs)
        try:
            life_cycle = client.get_bucket_lifecycle_configuration(Bucket = bucket);
            exists = True
            life_cycle_id = life_cycle['Rules'][0]['ID'];
            if life_cycle_id != 'delete1day':
                exists = False; 
        except botocore.exceptions.ClientError as e:
            error_code = e.response['Error']['Code'];
            if error_code == "NoSuchLifecycleConfiguration":
                exists = False 
        
        if not exists:
            kwargs = {'Bucket': bucket,
                'LifecycleConfiguration': {
                    'Rules': [
                        {
                            'Expiration': {
                                'Days': 1
                            },
                            'ID': 'delete1day',
                            'Prefix': '',
                            'Status': 'Enabled',
                        },
                    ]
                }
            }
            client.put_bucket_lifecycle_configuration(**kwargs);