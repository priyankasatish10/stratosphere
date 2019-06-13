# encoding: utf-8
"""Demonstrates how to make a simple call to the Natural Language API."""
import argparse
import csv
import re
import sys  
import json
import random
import time
from datetime import datetime


from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from datetime import datetime, timedelta
from nltk.tokenize import WordPunctTokenizer
tok = WordPunctTokenizer()
pat1 = r'@[A-Za-z0-9]+'
pat2 = r'https?://[A-Za-z0-9./]+'
combined_pat = r'|'.join((pat1, pat2))

def clean_tweets(text):
    #removing hashtags
    newtext= re.sub(r'#\w*','',text);
    #removing urls
    newtext= re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))','',newtext);
    #removing mentions
    newtext= re.sub(r'@\w*','',newtext);
    #removing emojis
    #newtext=re.sub(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])' , '',newtext);
        #removing smileys
    newtext=re.sub(r"(?:X|:|;|=)(?:-)?(?:\)|\(|O|D|P|S){1,}",'',newtext);
        #removing numbers
    newtext=re.sub(r"(^|\s)(\-?\d+(?:\.\d)*|\d+)",'',newtext);
        #removing resreved words
    newtext=re.sub(r'^(RT|FAV)','',newtext);

    newtext = re.sub(r':', '', newtext);
    newtext = re.sub(r'‚Ä¶', '', newtext);
        # replace consecutive non-ASCII characters with a space
    newtext = re.sub(r'[^\x00-\x7F]+', ' ', newtext);
    return newtext

def analyze(movie_review_filename):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()
    myFile = open('results.csv', 'w') 
    with myFile:
        myFields = ['Review', 'Score', 'Magnitude']
        writer = csv.DictWriter(myFile, fieldnames=myFields) 
        writer.writeheader()
        with open(movie_review_filename, 'r+') as csv_file:
                    # Instantiates a plain text document.
                content = csv.reader(csv_file)
                review_list = [row[0] for row in content]
        
        #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        for row in review_list:  
                text = clean_tweets(row)
                #count = count + 1
                document = types.Document( content=text,type=enums.Document.Type.PLAIN_TEXT)
                # Detects the sentiment of the text
                sentiment = client.analyze_sentiment(document=document).document_sentiment
                writer.writerow({'Review' : text, 'Score': sentiment.score , 'Magnitude': sentiment.magnitude})
        #print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

             
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'movie_review_filename',
        help='The filename of the movie review you\'d like to analyze.')
    args = parser.parse_args()

    analyze(args.movie_review_filename)