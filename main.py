import os
from pathlib import Path

from dotenv import load_dotenv

from vk_image_publishing import get_upload_link, upload_image, save_uploaded_photo, publish_comics
from xkcd_comics_loading import get_comic_info, download_comic, get_comics_count, choose_random_comic


if __name__ == '__main__':
    load_dotenv()

    vk_access_token = os.getenv('VK-ACCESS-TOKEN')
    vk_group_id = os.getenv('VK-GROUP-ID')
    vk_api_version = os.getenv('VK-API-V')

    comics_count = get_comics_count()
    comic_num = choose_random_comic(comics_count)

    comic = get_comic_info(comic_num)
    author_comment = comic['alt']
    image_url = comic['img']

    image_filename = str(comic_num) + '.png'
    image_path = Path.cwd() / image_filename

    download_comic(image_url, image_path)

    upload_link = get_upload_link(
        vk_access_token,
        vk_group_id,
        vk_api_version
    )

    upload_image_result = upload_image(upload_link, image_path)
    image_server, image_photo, image_hash = upload_image_result.values()

    loaded_photo = save_uploaded_photo(
        vk_group_id,
        vk_access_token,
        image_server,
        image_photo,
        image_hash,
        vk_api_version,
    )

    post_id = publish_comics(
        vk_group_id,
        vk_access_token,
        author_comment,
        loaded_photo['id'],
        loaded_photo['owner_id'],
        vk_api_version,
    )
    os.remove(image_path)