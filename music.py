import boto3

def music_table(dynamodb=None):

	if not dynamodb:

		dynamodb = boto3.resource('dynamodb')

	table = dynamodb.create_table(
		TableName='music',

		KeySchema=[

			{

			'AttributeName': 'title',

			'KeyType': 'HASH' # Partition key

			},

			{

			'AttributeName': 'artist',

			'KeyType': 'RANGE' # Sort key

			}

		],

			AttributeDefinitions=[

			{

			'AttributeName': 'title',

			'AttributeType': 'S'

			},

			{

			'AttributeName': 'artist',

			'AttributeType': 'S'

			},

		],

		ProvisionedThroughput={

			'ReadCapacityUnits': 10,

			'WriteCapacityUnits': 10

		}

	)

	return table

if __name__ == '__main__':

    musictable = music_table()

    print("Table status:", musictable.table_status)