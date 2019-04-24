import requests
import revert as r
import json
import config
import sys, os
import subprocess

def check_up():
    r = requests.get('https://upload.dtom.dev')
    return r.status_code

def send_alert(message):
    payload = {'text': f'{message}'}
    r = requests.post(config.slack_url, data=json.dumps(payload))

def redeploy():
    sys.path.append(os.getcwd())
    #print(os.listdir("."))
    os.system('chmod +x deploy.sh')
    deploy_command = "ssh greenday@panoptes.xyz DBNAME=$DBNAME DBPASSWORD=$DBPASSWORD DBHOST=$DBHOST DBUSER=$DBUSER DBPORT=$DBPORT 'bash -s' < deploy.sh"
    process = subprocess.Popen(deploy_command.split(), stdout=subprocess.PIPE)
    return process.communicate()


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
