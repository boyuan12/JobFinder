import random
import string
import boto3
import os
import pathlib

s3 = boto3.resource("s3", aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"), aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY_ID"))

def random_str(n=20):
    return "".join([random.choice(string.ascii_letters) for s in range(n)])

def upload_s3(request):
    name = random_str(10)
    s3.Bucket("django-jobfinder").put_object(Key=name, Body=request.FILES["file"])
    return name

def get_s3(name):
    obj = s3.Object("django-jobfinder", name)
    return obj.get()
