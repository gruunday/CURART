![CURART LOGO](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/raw/master/docs/blog/images/CURART_WIDE.png)

[![pipeline status](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/badges/master/pipeline.svg)](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/commits/master) [![coverage report](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/badges/master/coverage.svg)](https://gitlab.computing.dcu.ie/doylet9/2019-ca400-XXXX/commits/master)

## Intro

This project is written in python 3 to attempt to match images and artworks. The purpose of this is to attempt to find people who are using images that are copywright, modified from original or find the source of an artwork. This is implemented using the OpenCV version of the SIFT algorithm. Therefore it is not for comercial use and purely a research project. 

The second aim of the project is to work fast as scale. 

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


## Additional Resources

- Git [cheat sheet](https://gitlab.computing.dcu.ie/sblott/local-gitlab-documentation/blob/master/cheat-sheet.md)
- Gitlab [CI environment](https://gitlab.computing.dcu.ie/sblott/docker-ci-environment) and it's [available software](https://gitlab.computing.dcu.ie/sblott/docker-ci-environment/blob/master/Dockerfile)
- Example projects with CI configured:
   * [Python](https://gitlab.computing.dcu.ie/sblott/test-project-python)
   * [Java](https://gitlab.computing.dcu.ie/sblott/test-project-java)
   * [MySql](https://gitlab.computing.dcu.ie/sblott/test-project-mysql)
