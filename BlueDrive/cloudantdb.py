#!/bin/env python
'''
Created on Jan 29, 2016

@author: Ruchi.U
'''
from cloudant.account import Cloudant; 
import hashing
import urllib2
import os
import datetime
import pytz
import security
from cloudant.document import Document

class CloudantDB:
    
    def upload_file(self, file):
        self.connect_to_db();
        return self.upload_file_to_db(file);
            
    def upload_file_to_db(self, file):
        
        file_name = file.filename;
        file_contenttype = file.content_type
        uploaded_file_content = file.read();
        with open(file_name, 'wb') as f:
            f.write(uploaded_file_content);
        fileEncrypt = security.FileEncryption();
        encrypted_file_path = fileEncrypt.encrypt_file(file_name);
        with open(encrypted_file_path, 'rb') as f:
            uploaded_file_content = f.read();
        hashed_content = hashing.hash_data(uploaded_file_content);
        file_hashed_content, version = self.get_file_if_exists(file_name);
        if(version > 0):
            if(hashed_content == file_hashed_content):
                return "File Already Exists";
        version += 1;
        date = datetime.datetime.now(pytz.timezone("US/Central"));
        fmt = "%Y-%m-%d %H:%M:%S %Z"
        last_modified_time = date.strftime(fmt);
        data = {
            'file_name': file_name,
            'hashed_content': hashed_content,
            'version': version,
            'last_modified_time': last_modified_time
            }
        my_doc = self.database.create_document(data);
        my_doc.put_attachment(file_name, file_contenttype, uploaded_file_content);
        if my_doc.exists():
            print "SUCCESS";
        return "File Uploaded Successfully";
    
    def download_file(self, file_name, version):
        
        selector = {
            "file_name": file_name,
            "version": version
        }
        fields = ["version","_id","last_modified_time"];
        data = self.database.get_query_result(selector=selector, fields=fields)
        for my_doc in data:
            print my_doc;
            id = my_doc["_id"]
            last_modified_time = my_doc["last_modified_time"]
        
        document_val = Document(self.database, id);
        with open(file_name, 'wb') as f:
            document_val.get_attachment(file_name, write_to=file_name, attachment_type='binary')
        fileDecrypt = security.FileEncryption();
        fileDecrypt.decrypt_file(file_name, file_name);
    
    def download_file_test(self, file_name, id):
        
        username = "f0ebf985-0718-42ab-81c8-d9a4749781fe-bluemix";
        password = "ac3a0938a28cc22062aff710e67f7e4d782b822ed41c11e7bc5aec5b4a4b10e1"
        url = "https://f0ebf985-0718-42ab-81c8-d9a4749781fe-bluemix.cloudant.com"
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm();
        password_mgr.add_password(None, url, username, password)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(password_mgr)))
        url_to_download = self.URL_TO_DOWNLOAD +"/files_data/"+ id + "/" + file_name;
        request = urllib2.Request(url_to_download)
        f = urllib2.urlopen(request)
        data = f.read();
        return data;
    
    def download_file_from_db(self, file_name, version):
        self.connect_to_db();
        return self.download_file(file_name, version);
    
    def get_file_if_exists(self, file_name):
        
        selector = { "file_name": file_name,
                    "version": {"$gt": 0}
                }
        fields = ["hashed_content", "version"]
        sort = [{"version":"asc"}]
        data = self.database.get_query_result(selector=selector, fields=fields, sort=sort)
        version = 0;
        file_contents = "";
        for doc in data:
            if(version < doc["version"]):
                version = doc["version"];
                file_contents = doc["hashed_content"];
        return file_contents, version;
    
    def connect_to_db(self):
        
        self.file_upload_path = os.path.dirname(__file__) + "\\templates\\file_downloads"
        self.URL_TO_DOWNLOAD = "https://f0ebf985-0718-42ab-81c8-d9a4749781fe-bluemix.cloudant.com"
        self.client = Cloudant()
        self.client.connect();
        self.session = self.client.session();
        self.database = self.client['files_data'];
        
    def disconnect_db(self):
        self.cloudant_account.logout();
        
    def list_all_in_db(self):
        list = []
        for doc in self.database:
            if 'file_name' in doc.keys():
                list.append(doc['file_name'])
        print list
        return list;