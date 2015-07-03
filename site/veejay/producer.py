from __future__ import unicode_literals
import json
import logging
import re
import urllib2
import urlparse
import subprocess
import time

from flask import current_app

from shitstream import db
from shitstream.models import Video, Weight
from shitstream.utils import temp_chdir


def create_video_from_youtube(key, post):
    vid = Video()
    vid.key = key
    vid.filename = key + '.mp4'
    origin_dict = { key : post[key] for key in ['person', 'title', 'created_at'] }
    vid.origin = json.dumps(origin_dict)
    return vid


def create_weights_for_videos(video):
    weight = Weight()
    weight.weight = 1
    weight.video = video
    return weight


def get_iff_posts():
    response = urllib2.urlopen('http://infoforcefeed.shithouse.tv/data/all')
    iff_posts = json.load(response)
    return iff_posts


def get_youtube_iff_posts(posts):
    youtube_regex = re.compile('https?://(www.)?youtube.com/watch\?')
    youtube_posts = filter(lambda p: youtube_regex.match(p['url']), posts)
    return youtube_posts


def youtube_key_from_url(url):
    query = urlparse.urlparse(url).query
    video_key = urlparse.parse_qs(query)['v'][0]
    return video_key


# To remove extraneous query params
def youtube_url_from_key(key):
    return 'http://www.youtube.com/watch?v=' + key

def get_new_videos():
    current_app.logger.info('Retrieving new youtube posts')
    iff_posts = get_iff_posts()[:100]
    youtube_posts = get_youtube_iff_posts(iff_posts)
    keyed_posts = { youtube_key_from_url(p['url']) : p for p in youtube_posts }
    existing_keys = [ v.key for v in Video.query.all() ]
    new_movie_keys = set(keyed_posts.keys()).difference(set(existing_keys))

    current_app.logger.info('New youtube keys: {}'.format(str(new_movie_keys)))
    for new_movie_key in new_movie_keys:
        current_app.logger.info('Adding {} to the database'.format(new_movie_key))
        new_video = create_video_from_youtube(new_movie_key, keyed_posts[new_movie_key])
        weight = create_weights_for_videos(new_video)
        db.session.add(new_video)
        db.session.add(weight)
        db.session.commit()

        current_app.logger.info('Downloading {}'.format(new_movie_key))
        movie_url = youtube_url_from_key(new_movie_key)
        with temp_chdir(current_app.config['MOVIE_DIR']):
            ytdl_cmd = 'youtube-dl --max-filesize 500M --id -i --download-archive shitstream-downloads "{}"'.format(movie_url)
            subprocess.call(ytdl_cmd, shell=True)

def run():
    current_app.logger.setLevel(logging.DEBUG)

    while True:
        current_app.logger.info('Getting new videos')
        get_new_videos()

        current_app.logger.info('Sleeping for 10 minutes')
        time.sleep(600)
