'''
Created on Apr 30, 2016

@author: Ruchi.U
'''
import boto3
class NoSQL_DB:
    
    def __init__(self):
        kwargs = {'endpoint_url': 'https://dynamodb.us-west-2.amazonaws.com','aws_access_key_id':'AKIAIRAB5ZYWDZMT3PXQ', 'aws_secret_access_key':'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', 'region_name':'us-west-2'}
        connection = boto3.resource('dynamodb', **kwargs)
        self.table = connection.Table('images')
        
    def insert_image(self, image_json):
        self.table.put_item(Item = image_json)
        
    def insert_comments(self, image_id, image_by, username, comment):
        self.table.update_item(
            Key={
                'id': image_id,
                'username': image_by
            },
            AttributeUpdates={
                'comments': {
                    'Value': [{"username": username, "comment": comment}],
                    'Action': 'ADD',
                }
            },
            ReturnValues="ALL_NEW"
        )
        
    def delete_image(self, image_id, username):
        self.table.delete_item(
            Key={
                'id': image_id,
                'username': username
            }
        )
        return "Deleted from Dynamodb"
        
    def get_all_items(self):
        response = self.table.scan(
            AttributesToGet=[
                'username', 'id', 'comments', 'link'
            ]
        )
        return response;