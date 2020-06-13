#!/usr/bin/env python3

import requests
import json


def get_data(api_link, result=[]):
    try:
        data = requests.get(api_link).json()
    except requests.exceptions.MissingSchema:
        return result
    result += data['results']
    return get_data(data['next'], result)

with open('.github/workflows/processed.json') as f:
    processed = json.load(f)


def process_tag(image, target_image, tag):
    for arch in tag['images']:
        if image in processed and \
           tag['name'] in processed[image] and \
           arch['architecture'] in processed[image][tag['name']] and \
           processed[image][tag['name']][arch['architecture']] == arch['digest']:
            continue
        print(tag['name'], arch['digest'])
        if image not in processed:
            processed[image] = {}
        if tag['name'] not in processed[image]:
            processed[image][tag['name']] = {}
        processed[image][tag['name']][arch['architecture']] = arch['digest']


def process_image(image, target_image):
    data = get_data(f'https://hub.docker.com/v2/repositories/{image}/tags')
    for result in data:
        process_tag(image, target_image, result)


def main():
    process_image('library/alpine', 'Andy-ch/alpine-nocache')
    with open('.github/workflows/processed.json', 'w') as f:
        json.dump(processed, f, indent=2, sort_keys=True)

if __name__ == '__main__':
    main()
