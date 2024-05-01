import requests as req
from config import ACCESSTOKEN

class VK:
    def __init__(self, token, owner_id, version='5.131') -> None:
        self.owner_id = owner_id
        self.token = token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version, 'album_id': 'profile'}


    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.owner_id}

        response = req.get(url, params={**self.params, **params})

        return response.json()
   
    
    def save_photos(self, data):
         if 'response' in data:
            photos = data['response']['items']
            for photo in photos:
                sizes = photo['sizes']
                photo_url = next((size['url'] for size in sizes if size['type'] in ['z', 'y']), None)
                if photo_url:
                    filename = photo_url.split('/')[-1].split('?')[0]
                    response = req.get(photo_url)
                    if response.status_code == 200:
                        with open(filename, 'wb') as f:
                            f.write(response.content)
                            print(f"Saved photo: {filename}")
                    else:
                        print(f"Failed to download photo: {filename}")
                else:
                    print("No suitable photo URL found in sizes")
        

        

access_token = ACCESSTOKEN
owner_id = 7770471
vk = VK(access_token, owner_id)


data = vk.get_photos()

vk.save_photos(data)




