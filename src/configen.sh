#!/bin/bash

touch config.py
echo "dbname='$DBNAME'" > config.py
echo "user='$DBUSER'" >> config.py
echo "host='$DBHOST'" >> config.py
echo "port='$DBPORT'" >> config.py
echo "password='$DBPASSWORD'" >> config.py
