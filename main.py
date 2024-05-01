import requests as req
import json
from config import ACCESSTOKEN, YANDEXTOKEN


class VK:
    def __init__(self, token, owner_id, version='5.131') -> None:
        self.owner_id = owner_id
        self.token = token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version, 'album_id': 'profile', 'extended': 1}
        # Свойство для хранения счетчика лайков каждого элемента
        self.last_likes_count = None


    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id}

        response = req.get(url, params={**self.params, **params})

        return response.json()
   
    
    def save_photos(self, data):
         saved_photos_info = []
         if 'response' in data:
            photos = data['response']['items']
            for photo in photos:
                
                likes = photo['likes']['count']

                if self.last_likes_count is not None and likes == self.last_likes_count:
                    likes = photo['likes']['count'] + photo['date']

                sizes = photo['sizes']
                photo_url = next((size['url'] for size in sizes if size['type'] in ['z']), None)
                path = f'/Netology/{likes}'
                yandex = YandexRepository(path)
                yandex.yandex_save(photo_url, YANDEXTOKEN)                 
                self.last_likes_count = likes

                # Сохраняем информацию о файле
                obj = {
                    "file_name": f'{likes}.jpg',
                    "size": 'z'
                }
                saved_photos_info.append(obj)

         with open('json_data.json', 'w') as json_file:
                json.dump(saved_photos_info, json_file, indent=4)
                print(f"Файл записан: {json_file}.")


class YandexRepository:
    def __init__(self, path) -> None:
        self.path = path
    

    def yandex_save(self, url, auth):
        api_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

        headers = {
            'Authorization': f'OAuth {auth}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        params = {
        'path': self.path,
        'url': url
        }

        try:
            response = req.post(api_url, headers=headers, params=params)
            response_data = response.json()

            if response.status_code == 202:
                upload_href = response_data['href']
                if upload_href:
                    print(f"Файл загружен на диск: {upload_href}")
                else:
                    print("Файл не найден")
            else:
                print(f"Ошибка: {response_data.get('message')}")
        except req.exceptions.RequestException as e:
            print(f"Ошибка: {e}")
            

access_token = ACCESSTOKEN
owner_id = 7770471
vk = VK(access_token, owner_id)
data = vk.get_photos()
vk.save_photos(data)

