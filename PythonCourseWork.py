import time
from tqdm import tqdm
import requests
import datetime
import json


class VkPhoto:
    def __init__(self, Vk_id, Vk_token, count_photo):
        if (isinstance(Vk_id, int)):
            self.Vk_id = Vk_id
        else:
            params = {
                'user_ids': Vk_id,
                'access_token': Vk_token,
                'v': 5.131
            }
            response = requests.get("https://api.vk.com/method/users.get", params=params)
            if response.status_code != 200:
                print('Ошибка')
            data = response.json()
            self.Vk_id = data['response'][0]['id']
        self.Vk_token = Vk_token
        self.vk_data = []
        self.count_photo = count_photo
        self.Url = "https://api.vk.com/method/photos.get?"

    def photos_get(self):
        params = {
            'owner_id': self.Vk_id,
            'access_token': self.Vk_token,
            'album_id': 'profile',
            'v': 5.131,
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count_photo
        }
        response = requests.get(self.Url, params=params)
        if response.status_code != 200:
            print('Ошибка')
        data = response.json()
        photo_list = []
        likes_list = []
        for photo in data['response']['items']:
            file_name = int(photo['likes']['count'])
            if file_name in likes_list:
                file_name = str(file_name) + "-" + str(
                    datetime.datetime.utcfromtimestamp(int(photo['date'])).strftime('%Y-%m-%dT%H:%M:%SZ')[ 0:10]) + '.jpg'
            else:
                file_name = str(file_name) + '.jpg'

            photo_list.append({'file_name': file_name,
                               'size': 'z',
                               'url': photo['sizes'][-1]['url']})
            likes_list.append(int(photo['likes']['count']))
        time.sleep(0.3)
        self.vk_data = photo_list

    def write_json(self):
        with open('photo_list.json', 'w') as f:
            json.dump(self.vk_data, f, ensure_ascii=False, indent=2)


class YandexPhoto:
    def __init__(self, Yandex_token, Yandex_folder):
        self.Yandex_token = Yandex_token
        self.Yandex_folder = Yandex_folder
        self.UrlYandex = "https://cloud-api.yandex.net/v1/disk/resources/"
        self.url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'

    def get_new_folder(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.Yandex_token)}
        params = {
            'path': self.Yandex_folder,
            'overwrite': 'true'
        }
        r = requests.put(self.UrlYandex, params=params, headers=headers)
        if r.status_code != 201:
            print(f"Папка с именем: '{r}' уже существует")
        else:
            print(f"Папка с именем '{self.Yandex_folder}' успешно создана")

    def upload_file_YaDisk(self):
        data = []
        with open('photo_list.json') as json_file:
            data = json.load(json_file)
        for el in tqdm(data):
            params = {'url': el['url'], 'path': self.Yandex_folder + '/' + el['file_name']}
            headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.Yandex_token)}
            response = requests.post(self.url_upload, params=params, headers=headers)
            time.sleep(1)


if __name__ == "__main__":
    Vk_id = input('Введите id пользователя или короткое имя страницы: ')
    Vk_token = input('Введите свой токен VK: ')
    count_photo = int(input('Введите количество скачиваемых фото: '))
    UserVk = VkPhoto(Vk_id, Vk_token, count_photo)
    UserVk.photos_get()
    UserVk.write_json()
    Yandex_token = input('Введите токен с Яндекс.Полигона: ')
    Yandex_folder = input('Введите название Яндекс-папки: ')
    UserYa = YandexPhoto(Yandex_token, Yandex_folder)
    UserYa.get_new_folder()
    UserYa.upload_file_YaDisk()
