
'''
Created on Feb 3, 2016

@author: Ruchi.U
'''
import boto3
import config
class AWS:
    
    def __init__(self):
        self.aws_resource = boto3.resource('s3')
        self.bucket = self.aws_resource.Bucket(config.BUCKET_NAME)
    
    def upload_file(self, file_path, file_name):
        self.bucket.upload_file(file_path, file_name, ExtraArgs={'ACL':'public-read'});
        return "File Uploaded Successfully"
    
    def delete_image(self, image_id):
        self.bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                    'Key': image_id
                    },
                ],
            },
        )
        return "File Deleted Successfully"