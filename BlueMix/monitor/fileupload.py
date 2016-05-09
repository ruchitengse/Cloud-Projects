'''
Created on Jan 26, 2016

@author: Ruchi.U
'''
import config;
import swiftclient.client as swiftclient
import os
import security;
import sys

class FileUpload:    
    def upload_file_to_cloud(self, file_path, encryptFile):
        
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        print("\n Container List");
        container_name = 'Files';
        if encryptFile:
            container_name = 'encrypted';
            fileEncryption = security.FileEncryption();
            file_path = fileEncryption.encrypt_file(file_path);
            file_name = os.path.basename(file_path);
        else:
            container_name = 'plain';
            file_name = os.path.basename(file_path);
        print file_path;
        print file_name;
        with open(file_path, 'rb') as f:
            file_content = f.read();
        connection.put_object(container_name, file_name, contents=file_content)
        object_val = connection.get_object(container_name, file_name);
        file_details = object_val[0];
        print "File Uploaded";
        print file_details['last-modified']
        print file_details['content-length']
        connection.close();
        
    def upload_files_to_cloud(self, file_path):
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        print("\n Container List");
        
        ## ENCRYPTED FILE
        encrypted_container_name = 'encrypted';
        fileEncryption = security.FileEncryption();
        encryfile_file_path = fileEncryption.encrypt_file(file_path);
        encrypted_file_name = os.path.basename(file_path)
        with open(encryfile_file_path, 'rb') as f:
            file_content = f.read();
        connection.put_object(encrypted_container_name, encrypted_file_name, contents=file_content)
        object_val = connection.get_object(encrypted_container_name, encrypted_file_name);
        file_details = object_val[0];
        print "Encrypted File Length: " + file_details['content-length']
        print "Encrypted file last modified: " + file_details['last-modified'];
        ## PLAIN FILE
        plain_container_name = 'plain';
        file_name = os.path.basename(file_path);
        with open(file_path, 'rb') as f:
            file_content = f.read();
        connection.put_object(plain_container_name, file_name, contents=file_content)
        object_val = connection.get_object(plain_container_name, file_name);
        file_details = object_val[0];
        print "File Uploaded";
        print "Plain file last modified: " + file_details['last-modified']
        print "Plain file length: " + file_details['content-length']
        connection.close();
        
    def list_all_files(self):
        print "Listing Files"
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        print("\n Container List");
        container_name = sys.argv[1]
        for data in connection.get_container(container_name)[1]:
            print data['name'];
            
    
    def delete_a_file(self):
        file_name = sys.argv[1];
        container = sys.argv[2];
        print "\n\n"
        print "Deleting "+file_name+" from " + container;
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        connection.delete_object(container, file_name);

f_upload = FileUpload();
# f_upload.list_all_files();
f_upload.delete_a_file();