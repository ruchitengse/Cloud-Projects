'''
Created on Jan 28, 2016

@author: Ruchi.U
'''
import config;
import swiftclient.client as swiftclient
import security;
import sys

class FileDownload:
        
    def download_file_from_cloud(self, file_name, fileDecrypt):
        
        if fileDecrypt:
            container = 'encrypted'
            file_name = file_name + ".gpg";
        else:
            container = 'plain';
        file_path = config.DOWNLOADED_FILES + file_name;
        connection = swiftclient.Connection(preauthurl='https://dal.objectstorage.open.softlayer.com/v1/AUTH_eed52f663a464dada34e0c509ca54a2d', preauthtoken=config.pre_auth_token);
        object = connection.get_object(container, file_name);
        print file_path;
        with open(file_path, 'wb') as file_to_be_downloaded:
            file_to_be_downloaded.write(object[1]);
        dictValue = object[0];
        print dictValue['last-modified']
        print dictValue['content-length'];
        if fileDecrypt:
            fileDecrypt = security.FileEncryption();
            fileDecrypt.decrypt_file(file_path, file_name);
            
fileDownload = FileDownload();
file_name = sys.argv[1];
container = sys.argv[2]
if container == "encrypted":
    fileDownload.download_file_from_cloud(file_name, True);
else:
    fileDownload.download_file_from_cloud(file_name, False);