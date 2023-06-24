import requests
import threading
from itertools import cycle
import random
import os
import sys
import time
import asyncio
import base64
from datetime import datetime
import json

os.system('cls || clear')
os.system('')

EXTENSIONS = ['mp3']


sound_names = ['N WORDS', 'YOOO']


def bypassHeader(token):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': '*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'X-Context-Properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6Ijk4OTkxOTY0NTY4MTE4ODk1NCIsImxvY2F0aW9uX2NoYW5uZWxfaWQiOiI5OTAzMTc0ODgxNzg4NjgyMjQiLCJsb2NhdGlvbl9jaGFubmVsX3R5cGUiOjB9',
        'Authorization': token,
        'X-Super-Properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRmlyZWZveCIsImRldmljZSI6IiIsInN5c3RlbV9sb2NhbGUiOiJmciIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQ7IHJ2OjEwMi4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzEwMi4wIiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTAyLjAiLCJvc192ZXJzaW9uIjoiMTAiLCJyZWZlcnJlciI6IiIsInJlZmVycmluZ19kb21haW4iOiIiLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTM2MjQwLCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ==',
        'X-Discord-Locale': 'en-US',
        'X-Debug-Options': 'bugReporterEnabled',
        'Origin': 'https://discord.com',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://discord.com/', 
        'Cookie': '__dcfduid=21183630021f11edb7e89582009dfd5e; __sdcfduid=21183631021f11edb7e89582009dfd5ee4936758ec8c8a248427f80a1732a58e4e71502891b76ca0584dc6fafa653638; locale=en-US',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'TE': 'trailers',
    }


token = input("Token?: ")

headers = bypassHeader(token)


def printfn(text):
    
    sys.stdout.write(f'\r{text}')
    sys.stdout.flush()

class VoiceClient: 
    def __init__(self):
        self.success = 0
        self.retries = 0
        self.failed = 0
        
        self.uploading = False
    
    def spam_play(self, channel_id, jayson):
        session = requests.Session()
        try:
            while True:
                printfn(f'Playing successes: {str(self.success)}, failed: {str(self.failed)}')
                r = session.post(f'https://discord.com/api/v9/channels/{channel_id}/voice-channel-effects', headers=headers, json=jayson)
                if r.status_code == 429:
                    try:
                        time.sleep(r.json()['retry_after'] /1000)
                    except:
                        pass
                elif r.status_code == 204:
                    self.success += 1
                    
                else:
                    self.failed += 1
                    break
                    
        except KeyboardInterrupt:
            os._exit(0)
    
        
    def get_default_sounds(self):
        r = requests.get(f'https://discord.com/api/v9/soundboard-default-sounds', headers=headers)
        if r.status_code != 200:
            return self.main()
        else:
            return r.json()

    async def spam_play_default_soounds(self):
        chan_ids = input("Channel ID?:  ")
        sounds = self.get_default_sounds()    
        for sound in sounds:
            
            payload = {
                "emoji_id": None,
                "emoji_name": sound['emoji_name'],
                "override_path": sound['override_path'],
                "sound_id": sound['sound_id']
            }
            
           
            try:
                threading.Thread(target=self.spam_play, args=(chan_ids, payload,)).start()
                
            except KeyboardInterrupt:
                await self.main()
        
        
                
    def upload_song_and_play(self, guild_id, songs, channel_id):
        name = random.choice(sound_names)
        with open(f'audios/{songs}', 'rb') as ifile:
            encoded_str = base64.b64encode(ifile.read())
                         
        
        json = {
            'name': name,
            'sound': f"data:audio/mp3;base64,{(encoded_str.decode('utf-8'))}",
            'volume': 0.9798401586755987,
        }
        
        while True:                
            r = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/soundboard-sounds', headers=headers, json=json) 
            if r.status_code == 429:
                try:      
                    time.sleep(r.json()['retry_after'])
                except:
                    pass
            else:
                if r.status_code == 201:
                    print(f'New sound created at guild [ {guild_id}  ]')
                    payload = {
                        'emoji_id': None,
                        'override_path': None,
                        'sound_id': r.json()['sound_id'],
                        'source_guild_id': guild_id

                    }
                    threading.Thread(target=self.spam_play, args=(channel_id, payload,)).start()
                    break
                else:
                    
                    break
                    
    async def song_and_play(self):
        guild_ids = input("Guild ID?:  ")
        chan_ids = input("Channel ID?:  ")
        
        picturess = [i for i in os.listdir("audios/") if any(i.endswith(ten) for ten in EXTENSIONS)]
        
        if 1 == len(picturess):
            for i in range(3):
                threading.Thread(target=self.upload_song_and_play, args=(str(guild_ids), picturess[0], chan_ids,)).start()

        else:
            for p in picturess:
                threading.Thread(target=self.upload_song_and_play, args=(str(guild_ids), p, chan_ids,)).start()           
           
    def upload_song(self, guild_id, songs):
        '''
        r = requests.get(f'https://discord.com/api/v9/guilds/{guild_id}/soundboard-default-sounds', headers=headers)
        print(r.json())
        '''
        name = random.choice(sound_names)
        with open(f'audios/{songs}', 'rb') as ifile:
            encoded_str = base64.b64encode(ifile.read())
                         
        
        json = {
            'name': name,
            'sound': f"data:audio/mp3;base64,{(encoded_str.decode('utf-8'))}",
            'volume': 0.9798401586755987,
        }
        
        while True:
         
                            
            r = requests.post(f'https://discord.com/api/v9/guilds/{guild_id}/soundboard-sounds', headers=headers, json=json) 
            if r.status_code == 429:
                try:      
                    time.sleep(r.json()['retry_after'])
                except:
                    pass
            else:
                if r.status_code == 201:
                    print(f'New sound created at guild [ {guild_id}  ]')
                    break
                else:
                    
                    break

    async def runner_upload(self):
        guild_ids = input("Guild ID?:  ")
        amt = input("How many sounds?:  ")
    
        picturess = cycle([i for i in os.listdir("audios/") if any(i.endswith(ten) for ten in EXTENSIONS)])
        for i in range(int(amt)):
            threading.Thread(target=self.upload_song, args=(str(guild_ids), next(picturess),)).start()                
                
    async def main(self):
        os.system('cls || clear')
        os.system('mode 90, 23 & title made by: lone#4279 (sound maker/spammer)')
        print('''

       \033[38;2;60;255;0m╔═╗┌─┐┬ ┬┌┐┌┌┬┐┌─┐       
       \033[38;2;90;255;0m╚═╗│ ││ ││││ ││└─┐         Made by: a1rlone (on discord)
       \033[38;2;120;255;0m╚═╝└─┘└─┘┘└┘─┴┘└─┘         Github : https://github.com/airlone
       \033[0m
            [1] Spam Upload Songs     
            [2] Spam play default sounds
            [3] upload songs and spam play
     
        ''')
        ch = input("[ > ] Choose:  ")
        if ch == "1":
            self.songs_uploaded = 0
            self.retries = 0
            self.failed = 0
            await self.runner_upload()           
            await asyncio.sleep(2)
            await self.main()
            
        elif ch == "2":
            await self.spam_play_default_soounds()
            
        elif ch == "3":
            await self.song_and_play()
        else:
            os._exit(0)
    
    
if __name__ == "__main__":
    asyncio.run(VoiceClient().main())
