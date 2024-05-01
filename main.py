import requests as req
import json
import logging
from config import VKACCESSTOKEN, YANDEXTOKEN


# Класс для получения и записи фотографий профия Вконтакте
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
   
    # Основной метод программы который записывает полученные фотографии
    def save_photos(self, data) -> None:
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
                logging.info('Отправка файла в Яндекс репозиторий')
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
                logging.debug(f" Отладочный файл записан: {json_file}.")


# Класс для записи фотографий в Яндекс репозиторий
class YandexRepository:
    def __init__(self, path) -> None:
        self.path = path
    
    # Метод использующий Яндекс REST API для записи фотографий на диск Папка /Netology
    def yandex_save(self, url, auth) -> None:
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
                    logging.info(f"Файл загружен на Яндекс диск: {upload_href}")
                else:
                    logging.info("Файл не найден")
            else:
                logging.info(f"Ошибка: {response_data.get('message')}")
        except req.exceptions.RequestException as e:
            logging.info(f"Ошибка: {e}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

    access_token = VKACCESSTOKEN
    owner_id = 7770471
    vk = VK(access_token, owner_id)
    data = vk.get_photos()
    vk.save_photos(data)