#!/bin/bash

touch config.py
echo "dbname='$DBNAME'" > config.py
echo "user='$DBUSER'" >> config.py
echo "host='$DBHOST'" >> config.py
echo "port='$DBPORT'" >> config.py
echo "password='$DBPASSWORD'" >> config.py
echo "slack_url='$SLACK_URL'" >> config.py
echo "gitlab_token='$GITLAB_TOKEN'" >> config.py
