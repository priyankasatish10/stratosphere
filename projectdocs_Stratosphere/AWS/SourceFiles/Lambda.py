from __future__ import print_function

import base64
import json
import boto3



def lambda_handler(event, context):
    output = []

    for record in event['records']:
        dict_data = json.loads(base64.b64decode(record['data']).decode('utf-8').strip())


        comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
        sentiment_all = comprehend.detect_sentiment(Text=dict_data["text"], LanguageCode='en')
        sentiment = sentiment_all['Sentiment']
        print(sentiment)
        positive = sentiment_all['SentimentScore']['Positive']
        negative = sentiment_all['SentimentScore']['Negative']
        total = positive + negative/2


        data_record = {
            'message': dict_data["text"],
            'created_at': dict_data["created_at"],
            'location': dict_data["location"],
            'sentiment': sentiment,
            'total': total
        }

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')
        }


        output.append(output_record)
        
    return {'records': output}