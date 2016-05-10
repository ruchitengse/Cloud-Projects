'''
Created on Apr 29, 2016

@author: Ruchi.U
'''
import MySQLdb

class MySQL_DB:
    
    def __init__(self):
        self.connection = MySQLdb.connect(host="",user="",passwd="",db="users",port=3306)
        print self.connection
    
    def disconnect_from_mysql_db(self):
        self.connection.close()
        
    def create_user(self, username, password):
        cursor = self.connection.cursor()
        sql = "INSERT INTO user_creds (username, password) VALUES ('%s','%s')" % (username, password)
        try:
            cursor.execute(sql)
            self.connection.commit()
            return True
        except:
            self.connection.rollback()
            return False
            
    def verify_login(self, username, password):
        cursor = self.connection.cursor()
        sql = "SELECT username, password FROM user_creds WHERE username = '%s' AND password = '%s'" % (username, password)
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            if results:
                return True
        except:
            print "Error: Unable to fetch data"
        return False