from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django_otp.plugins.otp_totp.models import TOTPDevice

from ...otp_utils import render_terminal_qr


class Command(BaseCommand):
    help = 'Enroll a Django administrator with a TOTP authenticator app.'

    def add_arguments(self, parser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(username=options['username'])
        except user_model.DoesNotExist as exc:
            raise CommandError('The requested user does not exist.') from exc

        if not user.is_staff:
            raise CommandError('The requested user is not a Django administrator.')

        device, _ = TOTPDevice.objects.get_or_create(
            user=user,
            name='admin-authenticator',
            defaults={'confirmed': False},
        )

        if device.confirmed:
            self.stdout.write(self.style.WARNING('This administrator already has a confirmed TOTP device.'))
            return

        self.stdout.write('Scan this QR code with an authenticator app:')
        self.stdout.write(render_terminal_qr(device.config_url))
        token = input('Enter the current six-digit code to confirm enrollment: ').strip()

        if not device.verify_token(token):
            raise CommandError('Invalid authentication code; the device was not confirmed.')

        device.confirmed = True
        device.save(update_fields=['confirmed'])
        self.stdout.write(self.style.SUCCESS('TOTP authentication is enabled for this administrator.'))
