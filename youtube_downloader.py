"""Download all video's from a YouTube user to the hard drive.

This module uses BeautifulSoup4 to scrape links to all videos of a
user's YouTube channel, compares the titles of these links with the
videos present in the output directory and downloads the missing ones
using pytube.

To use this module, open a user's video page and scroll all the way down
to load all video's in the screen. Then save the page as HTML file
("Complete") to this module's directory. Then enter the path to the file
in "input_path", make sure that "output_path" is correct and press play.

Example video page: https://www.youtube.com/user/yogawithadriene/videos
"""

import os
import subprocess

from bs4 import BeautifulSoup
from pytube import YouTube
from pytube.exceptions import RegexMatchError


def get_links_from_file(html_file):
    """Scrape all video links and titles from the given HTML file.
    """

    with open(input_path) as input_file:
        soup = BeautifulSoup(input_file, 'html.parser')

    video_links = soup.find_all('a', id='video-title')
    videos = {}

    for link in video_links:
        videos[link['title']] = link['href']

    return videos


def get_new_titles(directory, titles):
    """Compares the list of titles with the videos in the directory and
    returns a list containing only the ones that aren't present yet.
    """

    new_titles = [
        title for title in titles
        if not file_exists_in_directory(title, directory)]

    return new_titles


def file_exists_in_directory(file, directory):
    """Checks the directory for a file with the same name as file and
    returns True or False.
    """

    files_in_directory = os.listdir(directory)

    # Cleanup file to match names of files in directory
    file = file\
        .replace('|', '')\
        .replace("'", '')\
        .replace(':', '')\
        .replace(',', '')\
        .replace('.', '')\
        .replace('...', '')

    # Cleanup names of files in directory to match file
    files_in_directory = [
        file_name
            .replace('.mp4', '')
            .replace(' - YouTube', '')
        for file_name in files_in_directory]

    return file in files_in_directory


def download_video(url, output_path):
    """Downloads the lowest resolution of a YouTube video containing both
    audio and video from `url` to `output_path` using PyTube
    """

    youtube_video = YouTube(url)
    stream = youtube_video.streams.get_lowest_resolution()

    if stream is None:
        raise IOError('No stream with video and audio found for {}'
                      .format(youtube_video.title))

    stream.download(output_path)


input_path = 'input/20200324_yogawithadrienne.html'
output_path = '/Users/harmtemolder/STACK/Videos/Yoga with Adrienne'

all_videos = get_links_from_file(input_path)
new_titles = get_new_titles(
    output_path,
    list(all_videos.keys()))

new_videos = {title: all_videos[title] for title in new_titles}

count = 0

for video_title, video_url in new_videos.items():
    count += 1

    print('Downloading {} ({} of {})'.format(
        video_title,
        count,
        len(new_videos)))

    try:
        download_video(
            video_url,
            output_path)
    except RegexMatchError as e:
        print('{}, skipping video...'.format(e))

# In Mac OSX 10.6 and higher, reveal the output directory in Finder
print('Download finished, opening output path in Finder')
subprocess.call(["open", "-R", output_path])
