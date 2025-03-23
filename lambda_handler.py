import boto3
import pymysql
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

# AWS & DB config
s3 = boto3.client('s3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket_name = "capclaim-uploads-prannov"
db = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB"),
    port=int(os.getenv("MYSQL_PORT"))
)

def upload_to_s3(file_path, s3_key):
    s3.upload_file(file_path, bucket_name, s3_key)
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    logging.info(f"Uploading file {file_path} to S3 as {s3_key}")
    return s3_url

def insert_claim(data):
    with db.cursor() as cursor:
        sql = """
        INSERT INTO claims (name, email, claim_type, description, image_url, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data['name'],
            data['email'],
            data['claim_type'],
            data['description'],
            data['image_url'],
            datetime.now()
        ))
        db.commit()
        logging.info(f"Inserting claim record into database for {data['email']}")
        print(f"Inserted claim for {data['name']} into MySQL.")

def lambda_handler(event):
    file_path = event['file_path']
    s3_key = f"claims/{event['name'].replace(' ', '_')}_{int(datetime.now().timestamp())}.png"
    s3_url = upload_to_s3(file_path, s3_key)

    event['image_url'] = s3_url
    insert_claim(event)
    return {
        "statusCode": 200,
        "body": f"Claim submitted successfully. File uploaded to {s3_url}"
    }

# Example run
if __name__ == "__main__":
    sample_event = {
        "name": "Prannov Jamadagni",
        "email": "prannov@example.com",
        "claim_type": "Health",
        "description": "Hospital visit after minor injury.",
        "file_path": "sample-claim-doc.png" 
    }
    result = lambda_handler(sample_event)
    print(result)
