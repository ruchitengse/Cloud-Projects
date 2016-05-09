#!/bin/env python
'''
Created on Mar 8, 2016

@author: Ruchi.U
'''
import hashlib;
import gnupg;
import os;
import config;

def hash_data(file_data):
    m = hashlib.sha224(file_data);
    return m.hexdigest();
     
def encrypt_file(file_path):    
    ## Generate key
    gpg = gnupg.GPG(gnupghome='/home/ubuntu/test');
    print file_path;
    file_name = os.path.basename(file_path);
    print file_name;
    print "Print 1"
    encrypted_file = file_name + ".gpg";
    print "Print 2"
    encrypted_file_path = os.path.join(config.ENCRYPTED_FILE_PATH, encrypted_file);
    with open(file_path, 'rb') as file_to_be_uploaded:
        status = gpg.encrypt_file(file_to_be_uploaded, recipients=['ruchi.tengse@hotmail.com'], output=encrypted_file_path, armor=False, passphrase='awss3');
    print "Print 3"
    return encrypted_file_path;
 
def decrypt_file(file_path, file_name):
    gpg = gnupg.GPG(gnupghome='/home/ubuntu/test');
    downloaded_file_path = os.path.join(config.DECRYPTED, file_name);
    with open(file_path, 'rb') as file_to_be_downloaded:
        status = gpg.decrypt_file(file_to_be_downloaded, passphrase = 'awss3', output=downloaded_file_path);
    return downloaded_file_path;