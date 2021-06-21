from configargparse import ArgParser

parser = ArgParser()

parser.add_argument(
    'course_url',
    action='store',
    help='Laracasts course url'
)

parser.add_argument(
    '-o',
    '--output',
    dest='output_dir',
    action='store',
    default='.',
    help='The output directory(default: Current Directory)'
)

args = parser.parse_args()