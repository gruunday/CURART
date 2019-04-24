import config
import requests
import json
import subprocess
import sys

def get_last_commit():
    r = requests.get('https://gitlab.computing.dcu.ie/api/v4/projects/doylet9%2F2019-ca400-doylet9/jobs?scope[]=success', headers={'PRIVATE-TOKEN': f'{gitlab_token}'})
    parsed = json.loads(r.text)
    return parsed[0]['commit']['id'], parsed[0]['finished_at']
    
def reset_head(last_commit):
    gitResetCommand = f'git reset --hard {last_commit}'
    process = subprocess.Popen(gitResetCommand.split(), stdout=subprocess.PIPE)
    return process.communicate()

def send_alert(message):
    r = requests.post(config.slack_url, data=json.dumps(message))

def revert_commit():
    last_commit, commit_time = get_last_commit()
    reset_head(last_commit)
    output, error = reset_head()
    if not error:
        text = "Encoutered error but reset to last known working version"
    else:
        text = f"PANIC: tried to reset to last known version but failed with error {error}"
    message = {'text': f'{text}'}
    send_alert(message)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        text = 'Test Alert'
        message = {'text': f'{text}'}
        send_alert(message)
    else:
        revert_commit()
