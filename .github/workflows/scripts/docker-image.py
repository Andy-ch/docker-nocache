#!/usr/bin/env python3

import os
import sys
import github3
import requests
import json

github = github3.login(token=os.environ['GH_PUSH_TOKEN'])
repository = github.repository(*os.environ['GITHUB_REPOSITORY'].split('/'))
processed_file_changed = False


def check_no_other_actions_running():
    res = requests.get(f'https://api.github.com/repos/{os.environ["GITHUB_REPOSITORY"]}/actions/workflows/docker-image.yml/runs?status=in_progress',
                       headers={'Authorization': f'token {os.environ["GITHUB_TOKEN"]}'})
    if res.json()['total_count'] > 1:
        print('Another run of this action is in progress. Exiting')
        sys.exit()


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
    global processed, processed_file_changed
    for arch in tag['images']:
        if image in processed and \
           tag['name'] in processed[image] and \
           arch['architecture'] in processed[image][tag['name']] and \
           processed[image][tag['name']][arch['architecture']] == arch['digest']:
            continue
        print(tag['name'], arch['architecture'], arch['digest'])
        if image not in processed:
            processed[image] = {}
        if tag['name'] not in processed[image]:
            processed[image][tag['name']] = {}
        processed[image][tag['name']][arch['architecture']] = arch['digest']
        processed_file_changed = True


def process_image(image, target_image):
    data = get_data(f'https://hub.docker.com/v2/repositories/{image}/tags')
    for result in data:
        process_tag(image, target_image, result)


def main():
    check_no_other_actions_running()
    if next(repository.commits()).message.find('[GH ACTION]') != -1:
        print('Latest commit was made by GH Action. Exiting')
        sys.exit()
    process_image('library/alpine', 'Andy-ch/alpine-nocache')
    processed_json = json.dumps(processed, indent=2, sort_keys=True).encode('utf-8')
    if processed_file_changed:
        repository.file_contents('/.github/workflows/processed.json').update('[GH ACTION] Update processed digests', processed_json)

if __name__ == '__main__':
    main()
