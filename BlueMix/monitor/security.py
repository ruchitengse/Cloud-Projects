'''
Created on Jan 27, 2016

@author: Ruchi.U
'''
import gnupg;
import os;
import config;
import test;

class FileEncryption:
    
    global gpg; 
        
    def encrypt_file(self, file_path):    
        ## Generate key
        gpg = gnupg.GPG(gnupghome='G:\\Test\\GNUPG');
        file_name = os.path.basename(file_path);
        encrypted_file = file_name + ".gpg";
        input_data = gpg.gen_key_input(passphrase='awss3', name_email='ruchi.tengse@hotmail.com');
        key = gpg.gen_key(input_data);
        encrypted_file_path = config.ENCRYPTED_FILE_PATH + encrypted_file;
        with open(file_path, 'rb') as file_to_be_uploaded:
            status = gpg.encrypt_file(file_to_be_uploaded, recipients=['ruchi.tengse@mavs.uta.edu'],output=encrypted_file_path);
        return encrypted_file_path;
     
    def decrypt_file(self, file_path, file_name):
        gpg = gnupg.GPG(gnupghome='G:\\Test\\GNUPG');
        downloaded_file_path = config.DOWNLOADED_FILES + file_name;
        with open(file_path, 'rb') as file_to_be_downloaded:
            status = gpg.decrypt_file(file_to_be_downloaded, passphrase = 'bluemix drive', output=downloaded_file_path);
            
        test.
f = FileEncryption()
f.encrypt_file("h")