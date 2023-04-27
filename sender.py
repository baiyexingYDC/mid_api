import requests
import yaml

from db import Db


class Sender:

    def __init__(self):
        self.db = Db()
        self.sender_initializer()

    def sender_initializer(self):
        # Load the yaml file
        with open('config.yaml') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.channelid=config['channelid']
        self.authorization=config['authorization']
        self.application_id = config['application_id']
        self.guild_id = config['guild_id']
        self.session_id = config['session_id']
        self.version = config['version']
        self.id = config['id']
        
        
    def send(self, data):
        header = {
            'authorization': self.authorization
        }

        #拼装mj参数
        prompt = data.get("prompt", "")
        params = " ".join(data.get("params", []))
        prompt = prompt + ' ' + params
        #保存到数据库并记录id
        self.db.add_mj_prompt_task(prompt)

        payload = {'type': 2, 
        'application_id': self.application_id,
        'guild_id': self.guild_id,
        'channel_id': self.channelid,
        'session_id': self.session_id,
        'data': {
            'version': self.version,
            'id': self.id,
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt)}],
            'attachments': []}
            }
        
        r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)
        while r.status_code != 204:
            r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)

        print('prompt [{}] successfully sent!'.format(prompt))
