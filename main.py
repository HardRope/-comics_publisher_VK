import os

from dotenv import load_dotenv
import requests
from pathlib import Path

def create_directory(main_dir ='image'):
    file_path = Path.cwd() / main_dir
    Path.mkdir(file_path, parents=True, exist_ok=True)
    return file_path


def get_comics_info(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_comics(url, path):
    response = requests.get(url)
    response.raise_for_status()
    with open(path, 'wb') as file:
        file.write(response.content)


def get_upload_link(token, group_id):
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': '5.131',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response']['upload_url']

def upload_image(url, path):
    with open(path, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()

def save_uploaded_photo(group_id, token, saved_data):
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': '5.131',
        'server': saved_data['server'],
        'photo': saved_data['photo'],
        'hash': saved_data['hash'],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK-ACCESS-TOKEN')
    vk_group_id = os.getenv('VK-GROUP_ID')

    url = 'https://xkcd.com/353/info.0.json'

    author_comment = get_comics_info(url)['alt']
    image_url = get_comics_info(url)['img']
    image_path = create_directory() / '353.png'

    download_comics(image_url, image_path)

    upload_link = get_upload_link(vk_access_token, vk_group_id)
    upload_result = upload_image(upload_link, image_path)
    save_uploaded_photo(vk_group_id, vk_access_token, upload_result)