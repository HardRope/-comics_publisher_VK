import requests

def get_upload_link(token, group_id, api_version='5.131'):
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


def save_uploaded_photo(group_id, token, saved_data, api_version='5.131'):
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


def publish_comics(group_id, token, message, media_id, owner_id, api_version='5.131'):
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
