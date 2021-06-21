# Laracasts_dl

Script to download Laracasts courses.

First of all, you need to install all requirements for this script using pip

    pip install beautifulsoup4 requests ConfigArgParse lxml





Help:

    usage: laracasts_dl.py [-h] [-o OUTPUT_DIR] course_url

    positional arguments:
    course_url            Laracasts course url

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT_DIR, --output OUTPUT_DIR
                            The output directory(default: Current Directory)
Example:

Downloading the course from url:

  
    laracasts_dl <url> -o <outpout_dir>

The "url" like: https://laracasts.com/series/laravel-6-from-scratch