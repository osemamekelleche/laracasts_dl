import requests
from bs4 import BeautifulSoup
import json
from .constants import *
import os
import sys
import shutil
import re


# Leading zeros depending on ep_count
def lzeros(number, ep_count):
    ep_count = str(ep_count)
    number = str(number)

    if len(number) == len(ep_count):
        return number
    else:
        return lzeros('0' + number, ep_count)


# Return human readable size of a file
def hrsize(size):
    kb = 1024
    mb = 1024 * kb
    gb = 1024 * mb
    size = int(size)
    if size < kb:
        return '%d B' % size
    elif size < mb:
        return '%.2f KB' % float(size / kb)
    elif size < gb:
        return '%.2f MB' % float(size / mb)
    else:
        return '%.2f GB' % float(size / gb)


def is_already_downloaded(dl_link, filename):
    if os.path.exists(filename) and os.path.isfile(filename):
        cur_size = int(os.stat(filename).st_size)
        filesize = int(requests.get(dl_link, stream=True).headers.get('Content-Length'))
        if cur_size == filesize:
            return True
    return False

def get_path_name(path_name):
    forbidden_chars = ['\\', '/', '?', '*', '"', '<', '>', '|', ':']
    for fc in forbidden_chars:
        if fc in path_name:
            path_name = path_name.replace(fc, '')
    return path_name

class Course:

    def __init__(self, url):
        self.url = url
        self.course = {}
        self.chapters = []

    def is_valid(self):
        self.url = self.url.strip('\'')
        if not self.url.startswith(BEGIN):
            return False
        if '/episodes' in self.url:
            return False
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, PARSER)
        json_data = soup.find('div', id='app')['data-page']
        json_data = json.loads(json_data)
        if 'series' not in json_data.get('props'):
            return False
        return True

    def download(self):
        content = requests.get(self.url).content
        soup = BeautifulSoup(content, PARSER)
        videos = soup.find('div', id='app')['data-page']
        self.course = json.loads(videos).get('props').get('series')
        course_name = get_path_name(self.course.get('title'))
        if not os.path.exists(course_name) or not os.path.isdir(course_name):
            os.mkdir(course_name)
        os.chdir(course_name)
        print('Downloading course: %s' %course_name)
        self.chapters = self.course.get('chapters')
        chapters_count = len(self.chapters)
        for i in range(chapters_count):
            self.download_chapter(i + 1, chapters_count)    
        print('Course: %s is completely downloaded' %course_name)

    def download_chapter(self, chapter_no, chapters_count):
        chapter_episodes = self.chapters[chapter_no - 1].get('episodes')
        ep_count = len(chapter_episodes)
        relative = 0
        if chapters_count > 1:
            chapter_title = self.chapters[chapter_no - 1].get('heading')
            chapter = '%s.%s' %(lzeros(chapter_no, chapters_count), get_path_name(chapter_title))
            print('\n\nDownloading chapter: %s' %chapter)    
            if chapter_no - 2 >= 0:
                relative = self.chapters[chapter_no - 2].get('count')
            if not os.path.exists(chapter) or not os.path.isdir(chapter):
                os.mkdir(chapter)
        for episode in chapter_episodes:
            if chapters_count > 1:
                os.chdir(chapter)
            self.download_episode(episode, episode.get('position') - relative, ep_count)
            if chapters_count > 1:
                os.chdir('..')
        if chapters_count > 1:    
            print('Chapter: %s downloaded' %chapter)

    def download_episode(self, episode, index, ep_count):
        protocol = '' if str(episode.get('download')).startswith('https:') else 'https:'
        dl_link = '%s%s' %(protocol, episode.get('download'))
        filename = '%s.%s.mp4' %(lzeros(index, ep_count), get_path_name(episode.get('title')))

        if is_already_downloaded(dl_link, filename):
            print('File: %s is already downloaded' % filename)
            return False

        cur_size = 0
        mode = 'wb'
        req = requests.get(dl_link, stream=True)

        if os.path.exists(filename) and os.path.isfile(filename):
            mode = 'ab'
            cur_size = int(os.stat(filename).st_size)
            headers = {
                'Range': 'bytes=%d-' % cur_size
            }
            req = requests.get(dl_link, headers=headers, stream=True)

        filesize = int(req.headers.get('Content-Length'))
        hrfilesize = hrsize(filesize + cur_size)
        print('\nDownloading file: %s\nFilesize: %s' % (filename, hrfilesize))

        with open(filename, mode) as f:
            data_len = 0
            chunk_size = 8192
            for data in req.iter_content(chunk_size):
                data_len += len(data)
                f.write(data)
                done = int(50 * float((data_len + cur_size) / (filesize + cur_size)))
                remaining = 50 - done
                percentage = 100 * float((data_len + cur_size) / (filesize + cur_size))
                percentage = '%.2f%%' % percentage
                text = '\r[%s%s] %s  %d/%d' % ('=' * done, ' ' * remaining,
                                               percentage, data_len + cur_size, filesize + cur_size)
                sys.stdout.write(text)
                sys.stdout.flush()
            print()
        return True