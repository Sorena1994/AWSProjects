import boto3
import requests 
import os

# Initialize AWS S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Define the number of images to download
        num_images_to_download = 50
        
        # Make API request
        url = "enter the url here" 
        headers = {
            enter data here like API key
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Upload images to S3
        bucket_name = bucketname
        
        for item in data:
            image_url = item['url']
            image_response = requests.get(image_url)
            image_key = f'bucketname/images/{os.path.basename(image_url)}'
            s3_client.put_object(Bucket=bucket_name, Key=image_key, Body=image_response.content)

        return {
            'statusCode': 200,
            'body': f'{num_images_to_download} images downloaded and uploaded to S3 successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
