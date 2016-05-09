'''
Created on Jan 28, 2016

@author: Ruchi.U
'''
from keystoneclient import session;
from keystoneclient.auth.identity import v3;
from keystoneclient.v3 import client;
import config;
import swiftclient.client as swiftclient
import os
import sys

class FileDownload:
        
    def download_file_from_cloud(self, file_name):
        
#         encrypted_file_name = file_name + ".gpg";
        file_path = config.DOWNLOADED_FILES + file_name;
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        object = connection.get_object('Files', file_name);
#         with open(file_path, 'w') as file_to_be_downloaded:
#             file_to_be_downloaded.write(object[1]);
        dictValue = object[0];
        response = "Last Modified: " + dictValue['last-modified'] + " Content Length: " + dictValue['content-length'];
        return response;
#         print dictValue['last-modified'] + 
#         print dictValue['content-length'];
#         fileDecrypt = security.FileEncryption();
#         fileDecrypt.decrypt_file(file_path, file_name);
    def get_users(self, inputline):
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        object = connection.get_object('Files', 'names.txt');
        values = object[0];
        for line in values.readline():
            if line == inputline:
                return "SUCCESS";
        return "FAILED";