# myapp/management/commands/runsql.py

import os
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Run an SQL file'

    def add_arguments(self, parser):
        parser.add_argument('sql_file', type=str, help='Path to the SQL file')

    def handle(self, *args, **kwargs):
        sql_file = kwargs['sql_file']

        if not os.path.exists(sql_file):
            self.stdout.write(self.style.ERROR(f"File '{sql_file}' does not exist"))
            return

        with open(sql_file, 'r') as file:
            sql = file.read()

        with connection.cursor() as cursor:
            cursor.execute(sql)

        self.stdout.write(self.style.SUCCESS(f"Successfully ran '{sql_file}'"))
