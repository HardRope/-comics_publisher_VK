# comics_publisher_VK
 
Program created to download random comic from [xkcd.com](https://xkcd.com/) and publish it with the author
comment at your [VK](https://vk.com) group, using VK-Api services.

## How to use

0. You have page on the social network [Vkontakte](https://vk.com) :)

1. Create your VK group [here](https://vk.com/groups?w=groups_create) or use your created 
group

2. Create app on [Vk-api](https://dev.vk.com/), type of app is `standalone ` and save 
this `client_id`

3. Get `access_token` [here](https://dev.vk.com/api/access-token/implicit-flow-user), you
must give your app permission to get next owns:
   - photos, 
   - groups, 
   - wall
   - offline

4. Download code, open console, go to code directory and install requirements

    ```
   pip install -r requirments.txt
   ```

5. Create `.env` file, contains next data:
   
    ```
    APP-ID='app_id'
    VK-API-V='current_api_v'        # default in programm - '5.131'
    VK-GROUP-ID='group_id'
    VK-ACCESS-TOKEN='a_long_string_with_token'
    ```

6. Run the program by console or in your preferred way. Run by console:

    ```
   python main.py
   ```
   
7. Check new post in your group.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
