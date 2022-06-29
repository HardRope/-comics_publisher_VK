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

if __name__ == '__main__':
    url = 'https://xkcd.com/353/info.0.json'

    image_url = get_comics_info(url)['img']
    image_path = create_directory() / '353.png'

    print(get_comics_info(url)['alt'])
    download_comics(image_url, image_path)