import boto3, json, os
from botocore.exceptions import NoCredentialsError
from botocore.client import Config as BotoConfig
from flask import Flask, request, jsonify, Blueprint, session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from decouple import config

from flask_login import (
    current_user,
    login_required
)

# TODO: create folder route


dreamobjects = Blueprint('dreamobjects', __name__)

upload_folder = os.getcwd()

key_id = config('DREAM0BJECTS_KEY')
region = config('DREAM0BJECTS_REGION_NAME')
profile_name = config('DREAM0BJECTS_PROFILE_NAME')
endpoint_url = config('DREAM0BJECTS_ENDPOINT_URL')
secret_key = config('DREAM0BJECTS_SECRET_KEY')


@dreamobjects.route('/upload-file', methods=["POST"])
@login_required
def uploadFile():
     print(request)
     if 'file_loc' in request.files.keys():
          bucket_name = session.get("user_id")
          file_upload =  request.files['file_loc']
          print(file_upload.filename)
          file_upload.save(secure_filename(file_upload.filename))

          config = BotoConfig(connect_timeout=600, retries={"mode": "standard"})

          sess = boto3.Session(region_name=region)

          s3 = sess.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url, config=config)
          s3.upload_file(upload_folder+"/"+file_upload.filename, bucket_name, file_upload.filename)

          return jsonify({"Status" : "File uploaded successfully", "file_name": file_upload.filename})   
     else:
          return jsonify({"error": "You're missing one of the following: file_loc, bucket_name ${bucket_name}"})
     
     

@dreamobjects.route('/delete-file', methods=["POST"])
@login_required
def deleteFile():
     bucket_name = session.get("user_id")
     file_name = request.form['file_name']

     sess = boto3.Session(region_name=region)

     s3 = sess.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)
     s3.delete_object(Bucket=bucket_name, Key=file_name)
     return jsonify({"Success": "File Deleted"})


@dreamobjects.route('/list-objects', methods=["POST"])
@login_required
def listObjects():
     bucket_name = session.get("user_id")
     sess = boto3.Session(region_name=region)
     s3 = sess.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)
     try:
          response = s3.list_objects(Bucket=bucket_name)
          object_names = []
          for obj in response['Contents']:
               object_names.append(obj['Key'])
          return jsonify(object_names)
     except:
          return jsonify({"Error": "Something went wrong"})
     

@dreamobjects.route('/download-file', methods=["POST"])
@login_required
def downloadFile():
     if 'file_name' in request.form.keys() and 'bucket_name' in request.form.keys():
          # bucket_name = request.form['bucket_name']
          bucket_name = session.get("user_id")
          file_name =  request.form['file_name']

          sess = boto3.Session(region_name=region)

          s3 = sess.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)

          with open(file_name, 'wb') as data:
             s3.download_fileobj(Bucket=bucket_name, Key=file_name, Fileobj=data)

          return jsonify({"Status" : "File downloaded successfully"})   
     else:
          return jsonify({"error": "You're missing one of the following: upload_file, bucket_name"})

@dreamobjects.route('/generate-link', methods=["POST"])
@login_required
def generateLink():
     if 'file_name' in request.form.keys():
          # bucket_name = request.form['bucket_name']
          bucket_name = session.get("user_id")
          file_name =  request.form['file_name']
          expiration_time = request.form['expiration_time']

          sess = boto3.Session(region_name=region)

          s3 = sess.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key, endpoint_url=endpoint_url)

          
          response = s3.generate_presigned_url('get_object',Params={'Bucket': bucket_name, 
                                                                 'Key': file_name},
                                                                 ExpiresIn=expiration_time)
          
          return response
     else:
          print(request.form.keys())
          return jsonify({"error": "Something went wrong"})

