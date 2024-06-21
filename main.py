import os
import requests
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):
    payload = {'v': '5.236', 'access_token': token, 'url': url}
    response = requests.get('https://api.vk.ru/method/utils.getShortLink',
                            params=payload)
    response.raise_for_status()

    shorten_link = response.json()['response']['short_url']
    return shorten_link


def count_clicks(token, link):
    payload = {
    	'v': '5.236',
    	'access_token': token,
    	'key': link,
    	'interval': 'forever'
    }
    response = requests.get('https://api.vk.ru/method/utils.getLinkStats',
                            params=payload)
    response.raise_for_status()

    clicks_count = response.json()['response']['stats'][0]['views']
    return clicks_count


def is_shorten_link(url):
    return 'vk.cc' in url


def main(url):
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    url = url.link

    if is_shorten_link(url):
        parsed_link = urlparse(url)
        try:
            clicks_count = count_clicks(token, parsed_link.path[1:])
        except requests.exceptions as error:
            print(error)
        else:
            print(f'По вашей ссылке прошли: {clicks_count} раз(а)')
    else:
        try:
            shortened_link = shorten_link(token, url)
        except requests.exceptions as error:
            print(error)
        else:
            print(f'Сокращенная ссылка: {shortened_link}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('link', nargs='?')
    url = parser.parse_args()
    main(url)
