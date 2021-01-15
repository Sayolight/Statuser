import json
import random
import os.path
import time

import requests
from PIL import Image
from dotenv import load_dotenv
from telethon import functions
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.types import InputPhoto, PeerChannel

load_dotenv()

print('Sayo.Statuser by Sayolight')

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
strg = os.getenv('JSON_STORAGE')
channel = int(os.getenv('CHANNEL'))

if not strg:
    newHeaders = {'Content-type': "application/json; charset=utf-8"}

    link = f'https://jsonbox.io/sayostatuser_{random.randint(1000000000, 2000000000)}/'
    response = requests.post(link,
                            data=json.dumps({'status': ''}),
                            headers=newHeaders)
    print(link+response.json()['_id'])

with TelegramClient('user', api_id, api_hash) as client:
    def update(s):
        p = client.get_profile_photos('me')
        if p:
            client(DeletePhotosRequest(
                id=[InputPhoto(
                    id=p[0].id,
                    access_hash=p[0].access_hash,
                    file_reference=p[0].file_reference
                )]
            ))
        ava = Image.open("photo.png")
        st = Image.open(f"img/{s}.png")
        width, height = ava.size
        w, h = st.size
        ava.paste(st, (int((width-w)/2), int((height-h)/2)), st)
        ava.save('status.png')
        client(functions.photos.UploadProfilePhotoRequest(
            file=client.upload_file('status.png'),
        ))


    while True:
        try:
            if strg:
                response = requests.get(f'{strg}')
                status = response.json()['status']
                if status and os.path.isfile(f'img/{status}.png'):
                    update(status)
                newHeaders = {'Content-type': "application/json; charset=utf-8"}

                response = requests.put(f'{strg}',
                                        data=json.dumps({'status': ''}),
                                        headers=newHeaders)

            msgs = client.get_messages(channel, limit=1)

            if msgs[0].message:
                cmd = msgs[0].message.lower().strip().split()
            else:
                cmd = None

            if cmd[0] == "help":
                client.edit_message(msgs[0], 'Thank You for using Statuser!\n\n' +
                                    'Commands list:\n' +
                                    '**s [STATUSNAME]** - set **[STATUSNAME].png** to avatar status\n')
            if cmd[0] == "s":
                channel_entity = client.get_entity(PeerChannel(channel))
                channel_info = client(GetFullChannelRequest(channel_entity))
                pinned_msg_id = channel_info.full_chat.pinned_msg_id

                if pinned_msg_id is not None:
                    posts = client(GetHistoryRequest(
                        channel_entity,
                        limit=1,
                        offset_date=None,
                        offset_id=pinned_msg_id + 1,
                        max_id=0,
                        min_id=0,
                        add_offset=0,
                        hash=0
                    ))
                    client.download_media(posts.messages[0], "photo.png")
                    if os.path.isfile(f'img/{cmd[1]}.png'):
                        update(cmd[1])
                        client.edit_message(msgs[0], "Обновлено!")
                        time.sleep(1)
                        msgs[0].delete()
                    else:
                        client.edit_message(msgs[0], f'Can\'t find **{cmd[1]}.png**')
        except:
            pass
        time.sleep(10)
