def sentiment_cloudfunction(data, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         data (dict): The dictionary with data specific to this type of event.
         context (google.cloud.functions.Context): The Cloud Functions event
         metadata.
    """
    import base64
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types

    tweet = ''
    if 'data' in data:
        try:
            tweet = base64.b64decode(data['data']).decode('utf-8')
        except Exception:
            tweet = data['data']
            print('not base64 encoded')
            pass

    # print('Hello {}!'.format(tweet))
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    # with open(movie_review_filename, 'r') as review_file:
    # Instantiates a plain text document.
    # content = review_file.read()
    content = tweet

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    # print(annotations)
    score = annotations.document_sentiment.score
    adjusted_score = (score + 1) * 5
    magnitude = annotations.document_sentiment.magnitude
    import json
    dic = {"tweet": str(tweet), "score": str(adjusted_score), "magnitude": str(magnitude)}
    print(json.dumps(dic))
    # print(adjusted_score);


