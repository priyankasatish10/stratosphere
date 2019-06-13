1. Create an instance on GCP under your project
2. SSH to the instance and run TwitterHelper.py
3. Create a topic in pub/sub for the project and ingest tweets.
4. Cloud function subscribed to the topic receives the tweets. Paste cloudfunction.py into the cloud function console. Cloud Natural Language API is invoked.
5. The scores are visible in the logging service of GCP.
6. Create another topic to stream the scores. Enable Logstash to receive this data through the subscription.
7. Create index on Kibana to view the logs stored in Elasticsearch

Excerpts of Twitterhelper.py is taken from Twitter website