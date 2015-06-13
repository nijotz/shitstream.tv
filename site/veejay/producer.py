from __future__ import unicode_literals
import json
import re
import urllib2
import urlparse
import subprocess

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


def run():
    iff_posts = get_iff_posts()[:100]
    youtube_posts = get_youtube_iff_posts(iff_posts)
    keyed_posts = { youtube_key_from_url(p['url']) : p for p in youtube_posts }
    existing_keys = [ v.key for v in Video.query.all() ]
    new_movie_keys = set(keyed_posts.keys()).difference(set(existing_keys))
    new_videos = [ create_video_from_youtube(key, keyed_posts[key]) for key in new_movie_keys ]
    weights = [ create_weights_for_videos(vid) for vid in new_videos ]
    db.session.add_all(new_videos)
    db.session.add_all(weights)
    db.session.commit()

    movie_urls = [youtube_url_from_key(key) for key in keyed_posts.keys()]
    with temp_chdir(current_app.config['MOVIE_DIR']):
        with open('shitstream-urls', 'w') as f:
            for url in movie_urls:
                f.write(url)
                f.write('\n')
        ytdl_cmd = 'youtube-dl --max-filesize 500M --id -i -a shitstream-urls --download-archive shitstream-downloads'
        subprocess.call(ytdl_cmd, shell=True)
