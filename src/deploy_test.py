import requests
import revert
import json

def check_up():
    r = requests.get('https://upload.dtom.dev')
    return r.status_code

def send_alert(message):
    slack_url = '{slack_url}'
    r = requests.post(slack_url, data=json.dumps(message))

def main():
    status = check_up()
    if status != 200:
        send_alert(f'Error responce from prod was {status} \n Trying to revert to last working commit')
    else:
        send_alert(f'Deployment Successful')

if __name__ == '__main__':
    main()
