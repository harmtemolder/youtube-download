#!/usr/bin/env python3

"""A simple command-line youtube downloader using `pytube`
"""

import os
from pathlib import Path
from pytube import YouTube  # https://pypi.org/project/pytubeX/
import sys
from urllib.parse import urlparse, parse_qsl


class YouTubeDownloader:
    def __init__(self, video_url):
        parsed_url = urlparse(video_url)
        parsed_qs = dict(parse_qsl(parsed_url.query))
        if 'v' in parsed_qs.keys():
            self.video_url = 'https://www.youtube.com?v={}'.format(parsed_qs['v'])
        else:
            raise ValueError('Unrecognized video_url')

    def __enter__(self):
        self.yt = YouTube(self.video_url)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:  # i.e. exiting because of an error
            pass
        pass

    def get_streams(self):
        audio_only = self.yt.streams.filter(only_audio=True)
        video_only = self.yt.streams.filter(only_video=True)
        both = self.yt.streams.filter(progressive=True)

        return {
           'audio_only': audio_only,
           'video_only': video_only,
           'both': both
        }

    def get_title(self):
        return self.yt.title

    def download(self, path, itag=None):
        if itag is None:
            stream = self.yt.streams.first()
        else:
            stream = self.yt.streams.get_by_itag(itag)

        stream.download(path)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
    else:
        youtube_url = input('Paste a link to a YouTube video: ')

    if len(sys.argv) > 3:
        output_dir = sys.argv[3]
    else:
        output_dir = Path(os.getcwd()).resolve()

    with YouTubeDownloader(youtube_url) as downloader:
        if len(sys.argv) > 2:
            itag = sys.argv[2]
        else:
            for filter_set, streams in downloader.get_streams().items():
                print(filter_set)
                for stream in streams:
                    print(end='\t')
                    print(stream)

            itag = input('Which stream do you want to download? Enter its '
                         '"itag": ')

        downloader.download(output_dir, itag)

        print('Successfully downloaded stream {} of "{}" ({}) into {'
              '}'.format(
            itag,
            downloader.get_title(),
            youtube_url,
            output_dir))
