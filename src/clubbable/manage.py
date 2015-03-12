#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    sys.path.append('../../submodules/attest')
    sys.path.append('../../submodules/django-attest')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clubbable.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
