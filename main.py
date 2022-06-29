import os
from pathlib import Path

from dotenv import load_dotenv
import requests

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


def get_upload_link(token, group_id, api_version):
    url = f'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
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


def save_uploaded_photo(group_id, token, api_version, saved_data):
    url = f'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'group_id': group_id,
        'access_token': token,
        'v': api_version,
        'server': saved_data['server'],
        'photo': saved_data['photo'],
        'hash': saved_data['hash'],
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['response'][0]


def publicate_comics(group_id, token, api_version, message, media_id, owner_id):
    url = f'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': f'-{group_id}',
        'access_token': token,
        'v': api_version,
        'message': message,
        'attachments': f'photo{owner_id}_{media_id}'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK-ACCESS-TOKEN')
    vk_group_id = os.getenv('VK-GROUP-ID')
    vk_api_version = os.getenv('VK-API-V')
    url = 'https://xkcd.com/353/info.0.json'

    author_comment = get_comics_info(url)['alt']
    image_url = get_comics_info(url)['img']
    image_path = create_directory() / '353.png'

    download_comics(image_url, image_path)

    upload_link = get_upload_link(vk_access_token, vk_group_id, vk_api_version)
    upload_result = upload_image(upload_link, image_path)
    loaded_photo = save_uploaded_photo(vk_group_id, vk_access_token, vk_api_version, upload_result)

    post_id = publicate_comics(
        vk_group_id,
        vk_access_token,
        vk_api_version,
        author_comment,
        loaded_photo['id'],
        loaded_photo['owner_id']
    )
