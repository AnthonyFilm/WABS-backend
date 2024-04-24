from functools import wraps
import secrets, boto3, json, os
from flask import Flask,request, jsonify, json
# from json import JSONEncoder
import decimal

from botocore.exceptions import NoCredentialsError
# from decouple import config

# from models import User

# key_id = config('DREAM0BJECTS_KEY')
# region = config('DREAM0BJECTS_REGION_NAME')
# profile_name = config('DREAM0BJECTS_PROFILE_NAME')
# endpoint_url = config('DREAM0BJECTS_ENDPOINT_URL')
# secret_key = config('DREAM0BJECTS_SECRET_KEY')

# def createBucket(bucket_name: str):

#      session = boto3.Session(region_name=region)
#      s3 = session.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)
#      try:
#           s3.create_bucket(Bucket=bucket_name)
#           return jsonify({"Success": "Bucket Created"})
#      except:
#           return jsonify({"Error": "Something went wrong"})
     
# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             return str(obj)
#         return super(JSONEncoder, self).default(obj)