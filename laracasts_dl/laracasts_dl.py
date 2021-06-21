from .functions import *
from .constants import *
from .commandline import args


def main():
    
    if not os.path.exists(args.output_dir) or not os.path.isdir(args.output_dir):
        print(f'"{args.output_dir}" does not exist or is not a directory.')
        exit(0)
    
    course = Course(args.course_url)
    
    os.chdir(args.output_dir)
    
    course.download()