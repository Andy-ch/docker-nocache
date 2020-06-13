#!/usr/bin/env python3

import requests


def get_tags(api_link, result=[]):
    try:
        data = requests.get(api_link).json()
    except requests.exceptions.MissingSchema:
        return result
    tags = result + [result['name'] for result in data['results']]
    return get_tags(data['next'], tags)


def process_image(image):
    tags = get_tags(f'https://hub.docker.com/v2/repositories/{image}/tags')
    print(tags)


def main():
    process_image('library/alpine')

if __name__ == '__main__':
    main()
