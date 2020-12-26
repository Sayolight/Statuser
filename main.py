import time
import json
import requests
from telethon import functions
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.types import InputPhoto
from PIL import Image

import os
from dotenv import load_dotenv

load_dotenv()

print('Sayo.Statuser by Sayolight')

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
strg = os.getenv('JSON_STORAGE')


if not strg:
    newHeaders = {'Content-type': "application/json; charset=utf-8"}

    response = requests.post('https://jsonstorage.net/api/items/',
                             data=json.dumps({'status': ''}),
                             headers=newHeaders)

    print(response.json())

with TelegramClient('user', api_id, api_hash) as client:

    def update(s):
        p = client.get_profile_photos('me')[0]
        client(DeletePhotosRequest(
            id=[InputPhoto(
                id=p.id,
                access_hash=p.access_hash,
                file_reference=p.file_reference
            )]
        ))
        ava = Image.open("photo.png")
        st = Image.open(f"img/{s}.png")

        ava.paste(st, (0, -1), st)

        ava.save('status.png')
        client(functions.photos.UploadProfilePhotoRequest(
            file=client.upload_file('status.png'),
        ))

    while True:
        try:
            for message in client.get_messages('me', limit=1):
                msg = message.message.split()

                if strg:
                    response = requests.get(f'https://jsonstorage.net/api/items/{strg}')
                    status = response.json()['status']
                    if status:
                        update(status)
                        newHeaders = {'Content-type': "application/json; charset=utf-8"}

                        response = requests.put(f'https://jsonstorage.net/api/items/{strg}',
                                                 data=json.dumps({'status': ''}),
                                                 headers=newHeaders)

                if msg[0] == "$upd":
                    client.download_profile_photo('me', "photo.png")
                    client.edit_message(message, 'Обновлено.')

                if msg[0] == "$s":
                    try:
                        update(msg[1])
                        message.delete()
                    except:
                        client.edit_message(message, 'Произошла ошибка.')
        except:
            pass
        time.sleep(10)
