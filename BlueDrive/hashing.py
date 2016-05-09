#!/bin/env python
'''
Created on Jan 29, 2016

@author: Ruchi.U
'''
import hashlib;

def hash_data(file_data):
    m = hashlib.sha224(file_data);
    return m.hexdigest();