from .functions import *
from .constants import *
from .commandline import args


def main():
    
    if not os.path.exists(args.output_dir) or not os.path.isdir(args.output_dir):
        print(f'"{args.output_dir}" does not exist or is not a directory.')
        exit(0)
    
    course = Course(args.course_url)
    
    if not course.is_valid():
        print(f'The url: "{args.course_url}" is not a valid course url')
        exit(0)

    os.chdir(args.output_dir)
    
    course.download()