from django.core.management.base import BaseCommand
import ip_tracking.models


class Command(BaseCommand):
    help = 'Block an IP address'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='The IP address to block')

    def handle(self, *args, **options):
        ip = options['ip']
        blocked, created = BlockedIP.objects.get_or_create(ip_address=ip)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip}'))
        else:
            self.stdout.write(self.style.WARNING(f'IP {ip} was already blocked'))