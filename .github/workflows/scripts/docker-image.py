#!/usr/bin/env python3

import os
import sys
import github3
import requests
import json
import subprocess
import multiprocessing

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
    rebuild_required = False
    platforms = []
    for arch in tag['images']:
        platforms.append(arch['architecture'])
        if arch['variant'] is None:
            arch['variant'] = ''
        if arch['architecture'] + arch['variant'] == '386':
            arch['architecture'] = 'i386'
        elif arch['architecture'] + arch['variant'] in ['armv6', 'armv7']:
            arch['architecture'] = 'arm32'
        if image not in processed or \
           tag['name'] not in processed[image] or \
           arch['architecture'] + arch['variant'] not in processed[image][tag['name']] or \
           processed[image][tag['name']][arch['architecture'] + arch['variant']] != arch['digest']:
            if image not in processed:
                processed[image] = {}
            if tag['name'] not in processed[image]:
                processed[image][tag['name']] = {}
            rebuild_required = True
            processed[image][tag['name']][arch['architecture'] + arch['variant']] = arch['digest']
            processed_file_changed = True
    if rebuild_required:
        platforms = list(set(platforms))
        process = subprocess.Popen(f'''set -xe
cd {image}
set +x
echo {os.environ['DOCKER_HUB_TOKEN']}|docker login -u andych --password-stdin
set -x
docker buildx build --platform {','.join(platforms)} -t {target_image}:{tag['name']} --build-arg tag={tag['name']} --push .''',
                                   shell=True)
        process.communicate()
        if process.returncode != 0:
            sys.exit(process.returncode)


def process_image(image, target_image):
    data = get_data(f'https://hub.docker.com/v2/repositories/{image}/tags')
    for result in data:
        process_tag(image, target_image, result)


def main():
    check_no_other_actions_running()
    process_image('library/alpine', 'andych/alpine-nocache')
    processed_json = json.dumps(processed, indent=2, sort_keys=True).encode('utf-8')
    if processed_file_changed:
        repository.file_contents('/.github/workflows/processed.json').update('[GH ACTION] Update processed digests', processed_json)

if __name__ == '__main__':
    main()
