import json
import boto3
import requests

def upload(music):

	for music in music['songs']:
         url = music['img_url']
         r = requests.get(url, stream=True)

         session = boto3.Session()
         s3 = session.resource('s3')

         bucket_name = 'storagea2'
         key = url.split('/')[::-1][0] # key is the name of file on your bucket

         bucket = s3.Bucket(bucket_name)
         bucket.upload_fileobj(r.raw, key)
			
if __name__ == '__main__':
	with open("a2.json") as json_file:

		music_list = json.load(json_file)
	upload(music_list)