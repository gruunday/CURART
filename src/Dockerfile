FROM gruunday/opencv-python3:latest

MAINTAINER Tom Doyle <thomas.doyle9@mail.dcu.ie>

RUN pip3 install Flask coverage boto3 psycopg2-binary gunicorn && mkdir -p /curart/tmp

ADD . /curart

WORKDIR /curart

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "curart:app"]
