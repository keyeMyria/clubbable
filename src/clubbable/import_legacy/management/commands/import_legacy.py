from django.core.management import BaseCommand
from import_legacy.import_legacy import import_legacy


class Command(BaseCommand):
    help = 'Imports from a legacy database'

    def add_arguments(self, parser):
        parser.add_argument('-x', '--excl-files', action='store_true',
                            help='Exclude documents and images')
        parser.add_argument('-p', '--path', help='Override path to files')

    def handle(self, *args, **options):
        incl_files = not options['excl_files']
        import_legacy(incl_files, options['path'])
