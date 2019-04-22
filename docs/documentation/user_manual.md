![CURART LOGO](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/CURART_WIDE.png)

# USER MANUAL

## Contents

1. Dependencies
2. How to use
3. Configuration
4. Help

## Dependencies
* This project depends on the following packages:
    - opencv
        - This is an image processing libraray, we are using the SIFT algorithm in the contrib_modules. This library is precompiled in the docker image
    - tlsh_hash
        - This is a locally sensitive hashing library. This allows us to hash keypoints and the resulting hashes will be similar if they are in fact similar key points
    - flask
        - This is the webframe work that is used to create the application
    - gunicorn
        - This is the production web server that is used to server the flask application
    - psycopg2-binary
        - A library to connect and query the postgres database


## How to use
* This application comes as part of a docker container
* To deploy just run 
    ```
    docker run gruunday/curart:latest
    ```
* **TODO** finish off this command with proper flags and options
