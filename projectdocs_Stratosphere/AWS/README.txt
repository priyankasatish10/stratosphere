Below are the steps to run the twitter analysis application on AWS
1. Launch EC2 Linux instance
2. Default installed version of python in linux AMI is 2.7. Applications needs python 3 and above as it uses boto 3 library.Install python 3.6 by executing following commands 
sudo yum install python36
sudo yum install python36-pip
3. Set python 3 as default version by executing command sudo update-alternatives --config python
4. Confirm the version by running python --version command
5. Install boto3 (SDK for AWS) by using command sudo pip install boto3
6. Install tweepy by using command sudo pip install tweepy
7. Create Lambda function on AWS with python 3.6 runtime. Paste the code from Lambda.py
9. Create Kinesis FireHose delivery stream and choose Source as Direct PUT and destination as Elastic Search Service. Choose to transform the records using Lambda option and specify the lambda function created in previous step.
10. Create a domain in Elastic Search Service with index as Comment and type as comment.Choose t2.small.elasticsearch as instance type and version as 6.5
11. Copy the python file TwitterStreaming.py on EC2 instance and run it using command python TwitterStreaming.py
12. Application can be monitored using logs created by lambda function under CloudWatchLogs.
13. One can confirm the data storage on elastic search by visiting indices tab on elastic search dashboard.
14. Graphs can be created using Kibana Visualization tool which is automatically deployed with elastic search domain.

