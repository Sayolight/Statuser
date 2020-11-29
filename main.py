import time
from telethon import functions
from telethon.sync import TelegramClient
from telethon.tl.functions.photos import DeletePhotosRequest
from telethon.tl.types import InputPhoto

import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

with TelegramClient('user', api_id, api_hash) as client:
    while True:
        for message in client.get_messages('me', limit=1):
            msg = message.message.split()
            if msg[0] == "$statuser":
                try:
                    p = client.get_profile_photos('me')[0]
                    client(DeletePhotosRequest(
                        id=[InputPhoto(
                            id=p.id,
                            access_hash=p.access_hash,
                            file_reference=p.file_reference
                        )]
                    ))
                    client(functions.photos.UploadProfilePhotoRequest(
                        file=client.upload_file(f'img/{msg[1]}.png'),
                    ))
                    message.delete()
                except:
                    client.edit_message(message, 'Произошла ошибка.')
        time.sleep(10)
