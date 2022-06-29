import os
from pathlib import Path

from dotenv import load_dotenv

from vk_image_loading import get_upload_link, upload_image, save_uploaded_photo, publicate_comics
from xkcd_comics_loading import get_comic_info, download_comic, get_comics_count, choose_random_comics

def create_directory(main_dir ='image'):
    file_path = Path.cwd() / main_dir
    Path.mkdir(file_path, parents=True, exist_ok=True)
    return file_path


if __name__ == '__main__':
    load_dotenv()
    vk_access_token = os.getenv('VK-ACCESS-TOKEN')
    vk_group_id = os.getenv('VK-GROUP-ID')
    vk_api_version = os.getenv('VK-API-V')

    comics_count = get_comics_count()
    comic_num = choose_random_comics(comics_count)

    comic = get_comic_info(comic_num)
    author_comment = comic['alt']
    image_url = comic['img']
    image_filename = str(comic_num) + '.png'
    image_path = create_directory() / image_filename

    download_comic(image_url, image_path)

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
    os.remove(image_path)