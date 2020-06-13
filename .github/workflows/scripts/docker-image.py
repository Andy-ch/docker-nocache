#!/usr/bin/env python3

import requests


def process_image(image):
    data = requests.get(f'https://hub.docker.com/v2/repositories/{image}/tags').json()
    print(data)


def main():
    process_image('library/alpine')

if __name__ == '__main__':
    main()
