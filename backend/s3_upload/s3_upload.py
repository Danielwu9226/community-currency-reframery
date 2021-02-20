#author: Daniel Wu

from secret import access_key, secret_key
import boto3
import os

def s3():
    #AWS S3 bucket connection
    client = boto3.client('s3',
                        aws_access_key_id = access_key,
                        aws_secret_access_key = secret_key)
    
    for file in os.listdir():
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".PNG") or file.endswith(".JPG") or file.endswith(".JPEG"):
             for image in file:
                AWS_STORE_BUCKET_NAME = "reframery-image"
                upload_file_key = 'user_images/' + str(file)
                client.upload_file(file, AWS_STORE_BUCKET_NAME, upload_file_key)
                #Object url
                url = (f'https://{AWS_STORE_BUCKET_NAME}.s3.amazonaws.com/{upload_file_key}')
            
    return url

#test output
# if __name__ == '__main__':
#     print(s3())
