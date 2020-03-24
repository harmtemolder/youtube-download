# youtube-download
 A Python script to download all videos from a single YouTube user

## How-to:
1. Open the YouTube page, e.g. https://www.youtube.com/user/yogawithadriene/videos
1. Keep scrolling down until all videos are shown on the page
1. Save the YouTube page as HTML in the input folder ("Web Page, Complete")
1. Check the values of the `input_path` and `output_path` variables in `youtube_downloader.py`
1. Run (⌃R in PyCharm) or debug (⌃D) `youtube_downloader.py`

## Troubleshooting:
* Make sure that you have the latest version of PyTube. Update by running these commands in your terminal:
  1. `source activate downloadyoutube`, or whichever environment you use to run `youtube_downloader.py` from
  1. `pip install pytube3` ([docs](https://python-pytube.readthedocs.io/en/latest/user/install.html))
* Sometimes a video will be downloaded with the filename "YouTube.mp4". Not sure why. Feel free to delete this and run `youtube_downloader.py` again