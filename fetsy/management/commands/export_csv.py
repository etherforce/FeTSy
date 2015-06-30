import csv

from django.core.management.base import BaseCommand, CommandError

from fetsy.models import Ticket


class Command(BaseCommand):
    args = '<filename>'
    help = 'Extracts all tickets and writes them to a CSV file.'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('You have to provide a filename.')
        output_file = open(args[0], 'w')
        csv_writer = csv.writer(output_file)
        csv_writer.writerow([
            'Id',
            'Content',
            'Tags',
            'Status',
            'Priority',
            'Assignee',
            'Created',
            'Period'])
        for ticket in Ticket.objects.all().select_related('assignee'):
            csv_writer.writerow([
                ticket.pk,
                ticket.content,
                ','.join(ticket.tags.splitlines()),
                ticket.get_status_display(),
                ticket.priority,
                ticket.assignee,
                ticket.created,
                ticket.period])
        output_file.close()
        self.stdout.write('CSV file written successfully.')
