import os
import boto3
import io

def s3(filepath, tried = 0):
    if tried > 5:
        return ""
    s3 = boto3.client('s3', aws_access_key_id="AKIXXXXXXXXXXXMKPXXXIDRA" , aws_secret_access_key="eYiNe8rjdXXXXXXXXXXXXXXXXXXQQnSPticxZMK")
    path = filepath[20:]
    try:
        s3.download_file('smartcartphoto',path, 'cart_read/'+ path)
        print("here")
    except:
        print("here2")
        return s3(filepath, tried + 1)
    return 'cart_read/'+ path