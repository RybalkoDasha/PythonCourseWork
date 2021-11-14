import time
from tqdm import tqdm
import requests
from pprint import pprint
import PySimpleGUI as sg


class VkPhoto:
    def __init__(self):
        self.Vk_id = int(input('Введите свой ID в VK: '))
        self.Vk_token = input('Введите свой токен VK: ')
        self.Yandex_token = input('Введите свой токен с Яндекс.Полигона: ')
        self.Yandex_folder = input('Введите название Яндекс-папки: ')
        self.vk_data = []
        self.count_photo = input('Введите количество скачиваемых фото: ')

    def photos_get(self):
        URL = "https://api.vk.com/method/photos.get?"
        params = {
            'owner_id': self.Vk_id,
            'access_token': self.Vk_token,
            'album_id': 'profile',
            'v': 5.131,
            'extended': 1,
            'photo_sizes': 1,
            'count': self.count_photo
        }
        response = requests.get(URL, params=params)
        if response.status_code != 200:
            print('Ошибка')
        data = response.json()
        photo_list = []
        for photo in data['response']['items']:
            photo_list.append({'file_name': str(photo['likes']['count']) + '-' + str(photo['date']) + '.jpg',
                               'size': 'z',
                               'url': photo['sizes'][-1]['url']})
        time.sleep(0.3)
        self.vk_data = photo_list
        pprint(self.vk_data)


    def get_new_folder(self):
        url = "https://cloud-api.yandex.net/v1/disk/resources/"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'OAuth {}'.format(self.Yandex_token)}
        params = {
            'path': self.Yandex_folder,
            'overwrite': 'true'
        }
        r = requests.put(url, params=params, headers=headers)
        if r.status_code != 201:
            print(f'Ошибка: {r}')
        else:
            print(f"Папка с именем '{self.Yandex_folder}' успешно создана")

    def upload_file_YaDisk(self):
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        for el in tqdm(self.vk_data):
            params = {'url': el['url'], 'path': self.Yandex_folder + '/' + el['file_name']}
            headers = {'Content-Type': 'application/json', 'Authorization': 'OAuth {}'.format(self.Yandex_token)}
            response = requests.post(url_upload, params=params, headers=headers)
            time.sleep(1)


YaUploader = VkPhoto()
YaUploader.photos_get()
YaUploader.get_new_folder()
YaUploader.upload_file_YaDisk()
