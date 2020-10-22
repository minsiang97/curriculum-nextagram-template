import boto3, botocore
from app import app
import braintree
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config.get("S3_KEY"),
   aws_secret_access_key=app.config.get("S3_SECRET")
)

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id= app.config.get("BT_MERCHANT_ID"),
        public_key=app.config.get("BT_PUBLIC_KEY"),
        private_key=app.config.get("BT_PRIVATE_KEY")
    )
)


def upload_file_to_s3(file, acl="public-read"):

    try:    
        s3.upload_fileobj(
            file,
            app.config.get("S3_BUCKET"),
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        
        print("Something Happened: ", e)
        return e

    return file.filename