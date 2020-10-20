import boto3, botocore
from config import ProductionConfig

s3 = boto3.client(
   "s3",
   aws_access_key_id=ProductionConfig.S3_KEY,
   aws_secret_access_key=ProductionConfig.S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        
        print("Something Happened: ", e)
        return e

    return "{}{}".format(ProductionConfig.S3_LOCATION, file.filename)