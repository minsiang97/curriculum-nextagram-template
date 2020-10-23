import boto3, botocore
import braintree
import os
from app import app
from authlib.integrations.flask_client import OAuth


oauth = OAuth()

oauth.register('google',
    client_id=app.config.get("G_CLIENT_ID"),
    client_secret=app.config.get("G_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)

oauth.init_app(app)

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