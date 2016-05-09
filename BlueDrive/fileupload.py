'''
Created on Jan 26, 2016

@author: Ruchi.U
'''
import config;
import swiftclient.client as swiftclient
import os
from downloadfile import FileDownload;
import hashing
import random

class FileUpload:    
    def upload_file_to_cloud(self, file):
        
        file_name = file.filename;
        file_content = file.read();
        hashed_content = hashing.hash_data(file_content);
        
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        print("\n Container List");
        container_name = 'Files';
        
        print "Check if file already exists"
        filename, file_extension = os.path.splitext(file_name)
        connection.get_object('Files', file_name);
        object = None;
        try:
            object = connection.get_object('Files', file_name);
            print object;
        except:
            print "File does not exist"
        if object:
            file_content = object[1];
            if file_content != hashed_content:
                file_name = filename + "_" + str(random.randrange(1, 100)) + file_extension;
            else:
                return "File Exists!"
        connection.put_object(container_name, file_name, contents=hashed_content)
        connection.close();
        
        fileDownload = FileDownload();
        response = fileDownload.download_file_from_cloud(file_name);
        return response;