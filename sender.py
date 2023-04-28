import json

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

        header = config['header']
        payload = config['payload']

        self.origin = header['origin']
        self.referer = header['referer']
        self.authorization = header['authorization']
        self.channelid = payload['channelid']
        self.application_id = payload['application_id']
        self.guild_id = payload['guild_id']
        self.session_id = payload['session_id']
        self.version = payload['version']
        self.id = payload['id']

    def send(self, data):
        header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'authorization': self.authorization,
            'content-type': 'application/json',
            'cookie': '__dcfduid=14630b6adfe911ed8faffa25186d30b8; __sdcfduid=14630b6adfe911ed8faffa25186d30b84c9e3a255c45c4c32234f0c97dd166a94260cc05688d1e9ace4162335adb6b38; __stripe_mid=65e78f87-21bc-47f9-8eaf-ef1abb7299442b1b92; _gid=GA1.2.1430313046.1682578175; OptanonConsent=isIABGlobal=false&datestamp=Thu+Apr+27+2023+14%3A49%3A36+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.33.0&hosts=; _ga=GA1.1.1849989381.1682578175; _ga_XXP2R74F46=GS1.1.1682578176.1.0.1682578178.0.0.0; __cfruid=6719600b3f19c7abae2ff086a52a5b332199c5b6-1682651457; __cf_bm=qu82FRUGdVyHxg6cPZc7KFxkyebvzgpkuuwnr1mZvRA-1682651463-0-AQQQlm8kzD3qwFMo80p5mI3PjgVrawnbazXNPu8A5sDLPcZH/ngHslHypui1BcjA8nUL5cDdsoCbxRMRY+9vC2tUZEEguDA8x8yAPu785gE7',
            'origin': self.origin,
            'referer': self.referer,
            'sec-ch-ua': '"Chromium";v="112", "Microsoft Edge";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'zh-CN',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InpoLUNOIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMi4wLjAuMCBTYWZhcmkvNTM3LjM2IEVkZy8xMTIuMC4xNzIyLjU4IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTEyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5taWRqb3VybmV5LmNvbS8iLCJyZWZlcnJpbmdfZG9tYWluIjoid3d3Lm1pZGpvdXJuZXkuY29tIiwicmVmZXJyZXJfY3VycmVudCI6Imh0dHBzOi8vd3d3Lm1pZGpvdXJuZXkuY29tLyIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6Ind3dy5taWRqb3VybmV5LmNvbSIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE5MzYwMCwiY2xpZW',
        }

        # 拼装mj参数
        prompt = data.get("prompt", "")
        params = " ".join(data.get("params", []))
        prompt = prompt + ' ' + params
        # 保存到数据库并记录id
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
                       'application_command': {
                           'id': self.id,
                           'application_id': self.application_id,
                           'version': self.version,
                           'default_member_permissions': None,
                           'type': 1,
                           'nsfw': False,
                           'name': 'imagine',
                           'description': 'Create images with Midjourney',
                           'dm_permission': True,
                           'contexts': None,
                           'options': [
                               {
                                   'type': 3,
                                   'name': 'prompt',
                                   'description': 'The prompt to imagine',
                                   'required': True
                               }
                           ]
                       },
                       'attachments': []}
                   }

        r = requests.post('https://discord.com/api/v9/interactions', data=json.dumps(payload), headers=header)
        while r.status_code != 204:
            r = requests.post('https://discord.com/api/v9/interactions', data=json.dumps(payload), headers=header)

        print('prompt [{}] successfully sent!'.format(prompt))
