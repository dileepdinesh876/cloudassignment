import json

import boto3

def load_music(music, dynamodb=None):

    if not dynamodb:

        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('music')

    for music in music['songs']:
        title = music['title']
        artist = music['artist']
        year = music['year']
        web_url = music['web_url']
        img_url = music['img_url']
	
        table.put_item(Item=music)
	
if __name__ == '__main__':
	with open("a2.json") as json_file:

		music_list = json.load(json_file)

	load_music(music_list)