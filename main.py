import requests as req
from config import ACCESSTOKEN, YANDEXTOKEN

class VK:
    def __init__(self, token, owner_id, version='5.131') -> None:
        self.owner_id = owner_id
        self.token = token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version, 'album_id': 'profile', 'extended': 1}


    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id}

        response = req.get(url, params={**self.params, **params})

        return response.json()
   
    
    def save_photos(self, data):
         if 'response' in data:
            photos = data['response']['items']
            for photo in photos:
                likes = photo['likes']['count']
                sizes = photo['sizes']
                photo_url = next((size['url'] for size in sizes if size['type'] in ['z']), None)
                path = f'/Netology/{likes}'
                yandex = YandexRepository(path)
                yandex.yandex_save(photo_url, YANDEXTOKEN)                 


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
                    print(f"File upload initiated. Upload link: {upload_href}")
                else:
                    print("Upload link not found in response")
            else:
                print(f"Error message: {response_data.get('message')}")
        except req.exceptions.RequestException as e:
            print(f"Error making request: {e}")
            
        

        

access_token = ACCESSTOKEN
owner_id = 7770471
vk = VK(access_token, owner_id)

data = vk.get_photos()

vk.save_photos(data)

# url = 'https://sun9-12.userapi.com/impg/c855120/v855120592/241212/IKJ6A9pcDes.jpg?size=75x56&quality=96&sign=ccb8dfab8b6bedfd2cd678a3af5119f0&c_uniq_tag=9gXAZfmcLIo43cHKqQitlTdLkDj947uQR1p-plJ7FBY&type=album'

# yandex = YandexRepository('/Netology')

# yandex.yandex_save(url, YANDEXTOKEN)
