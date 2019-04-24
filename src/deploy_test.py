import requests
import revert as r
import json
import config
import sys
import subprocess

def check_up():
    r = requests.get('https://upload.dtom.dev')
    return r.status_code

def send_alert(message):
    payload = {'text': f'{message}'}
    r = requests.post(config.slack_url, data=json.dumps(payload))

def redeploy():
    sys.exit(435)

def main():
    status = check_up()
    if status != 200:
        send_alert(f'Error responce from prod was {status} \n Trying to revert to last working commit')
        r.revert_commit()
        redeploy()
    else:
        send_alert(f'Deployment Successful')


if __name__ == '__main__':
    main()
